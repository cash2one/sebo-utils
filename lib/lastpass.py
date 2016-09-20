import os, configparser

import lib.drive
import lib.password_creator
import lib._lastpass.vault
import vars
import getpass

def _prompt_for_credentials():
    def save_username(username):
        try:
            vars.credentials_conf.set("lastpass", "username", username)
            with vars.credentials_conf_loc.open('w') as configfile:
                vars.credentials_conf.write(configfile)
        except configparser.NoSectionError:
            vars.credentials_conf.add_section("lastpass")
            vars.credentials_conf.set("lastpass", "username", username)
            with vars.credentials_conf_loc.open('w') as configfile:
                vars.credentials_conf.write(configfile)
    if not vars.lastpass_username:
        vars.lastpass_username = input("What's your lastpass username (your sebodev email): ")
        save_username(vars.lastpass_username)
    elif vars.verbose:
        save_username(vars.lastpass_username)

    vars.lastpass_password = retrieve_password()
    if not vars.lastpass_password or vars.verbose:
        vars.lastpass_password = getpass.getpass("what's your lastpass password: ") #getpass behaves like input(), except the user input is not displayed on the screen
        save_password(vars.lastpass_password)


def find(search_term, search_term2=None, exact_match=False):
    """A generator that finds lastpass passwords by username, urk, or name.
    Optionally narrow down the search by searching through the lastpass names of the results returned with search_term2
    Set exact match to true to only return matches if the name matches the search term exactly. search_term2 does nothing if exact_match is set."""
    search_term = str(search_term)
    if not (vars.lastpass_username and vars.lastpass_password) or vars.verbose:
        _prompt_for_credentials()
    else:
        vars.lastpass_password = retrieve_password()

    try:
        vault = lib._lastpass.Vault.open_remote(vars.lastpass_username, vars.lastpass_password)
    except lib._lastpass.exceptions.LastPassInvalidPasswordError:
        print("Couldn't connect to LastPass. Let's give it another go.")
        vars.lastpass_password = getpass.getpass("What's your LastPass password: ")
        vault = lib._lastpass.Vault.open_remote(vars.lastpass_username, vars.lastpass_password)
        save_password(vars.lastpass_password)


    if exact_match:
        for password_obj in vault.accounts:
            if search_term == password_obj.name.strip():
                yield password_obj
    else:
        for password_obj in vault.accounts:
            for term in search_term.split():
                if (
                        term in str(password_obj.name)
                        or term in str(password_obj.url)
                        or term in str(password_obj.username)
                    ):
                    if search_term2 and search_term2 in password_obj.name:
                        yield password_obj
                        break
                    else:
                        yield password_obj
                        break

        #there is also password_obj.id and password_obj.group


def save_password(password):
    """encrypts and saves password to a config file
    only works on Windows """
    #we use a simple encryption with a password key stored by Google Drive that can only be retreieved by authenticating with Google Drive
    #and we use a built-in encryption function to windows that only can be decrypted from a program run on the computer it was encrypted from
    #I don't know if there is any such function on Macs, so we'll just revert back to the defualt behaviour of asking the for a password each time on a mac
    if os.name == 'nt':
        try:
            import win32crypt
        except:
            if vars.verbose:
                print("If you don't want to have to type in the password each time, you can install the python extension from https://sourceforge.net/projects/pywin32/files/pywin32/Build%20220/ so I can more securely save the password on the computer")

        drive_dir = vars.google_drive_smash_utils_dir
        if not drive_dir.is_dir():
            drive_dir.mkdir()

        key_file = drive_dir / "lastpass-key-part1"
        key = lib.password_creator.create(20)
        key_file.write_text(key)

        encoded1 = win32crypt.CryptProtectData(password.encode()).hex()
        encoded2 = _encode(key, encoded1).hex()

        vars.credentials_conf.set('lastpass', 'password', encoded2)

        with vars.credentials_conf_loc.open('w') as configfile:
            vars.credentials_conf.write(configfile)

def retrieve_password():
    """retrieves a password saved with save_password
    only works on windows"""
    try:
        import win32crypt
    except:
        return

    password = vars.credentials_conf.get('lastpass', 'password', fallback=None)
    if not password:
        return

    key_file = vars.google_drive_smash_utils_dir / "lastpass-key-part1"
    key = key_file.read_text()
    password = _decode(key, bytes.fromhex(password).decode())

    password = win32crypt.CryptUnprotectData(bytes.fromhex(password))[1]

    return password.decode()


def _encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return "".join(enc).encode()

def _decode(key, enc):
    dec = []
    enc = enc
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)
