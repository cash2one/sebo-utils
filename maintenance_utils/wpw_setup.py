import shutil, os, re
import vars

# vars.wpw_name contains the client name passed in from the command line
# vars.wpw_level is a 1, 2, or 3 for the different wordpress warranty packages -- wpw 99, wpw+, and wpw & maintenance

client_dir = vars.google_drive_maintenance_dir / "clients" / vars.wpw_name
client_website_guess = vars.wpw_name.replace(" ", "").strip()
if re.search("(\....$)", client_website_guess) is None:
    client_website_guess += ".com"
client_website = input("what website is this for? Leave blank if it's {}: ".format(client_website_guess))
if not client_website:
    client_website = client_website_guess

def create_google_drive_folder():
    """create a folder for them in Google Drive
    The folder is a copy of _client folder template """
    try:
        client_template_dir = vars.google_drive_maintenance_dir / "clients" / "_client folder template"
        shutil.copytree(str(client_template_dir), str(client_dir))
        print("You can just hit ok on the Google Drive pop-up")
    except FileExistsError:
        response = input("%s already exists. Would you like to reconfigure this folder? This will delete some of the existing data [yes/No]:" % client_dir)
        if response.startswith("y"):
            pass
        else:
            print("okay, I'll leave your data alone")
            raise SystemExit

def create_contact_info_file():
    """create the contact info file, replacing it if it already exists"""

    contact_info_file = client_dir / "Contact Info.txt"

    try:
        os.remove(str(contact_info_file))
    except FileNotFoundError:
        pass

    print("\nHey, could I quickly get a little info about %s's point of contact" % vars.wpw_name)
    poc_name = input("what is the name of the point of contact: ")
    poc_email = input("What is {}'s email: ".format(poc_name))
    poc_phone = input("What is {}'s phone number: ".format(poc_name))
    poc_position = input("And What is {}'s position in the company (if known): ".format(poc_name))
    notes = input("Enter any other information you would like me to add to %s's contact info file: " % vars.wpw_name)

    contact_info_contents = '''Point of contact
    Name: {}
    Position: {}
    Email: {}
    Phone: {}

    notes: {}
    '''.format(poc_name, poc_position, poc_email, poc_phone, notes)
    contact_info_file.write_text(contact_info_contents)

def save_dns_info():
    import maintenance_utils.dns
    dns_file = client_dir / (client_website + " dns info.txt")
    print("client_website", client_website)
    maintenance_utils.dns.main(client_website, dns_file)



create_google_drive_folder()
create_contact_info_file()
save_dns_info()


# plugins_dir = vars.google_drive_maintenance_dir / "Maintenance Setup" / "Plugins"
# subprocess.call(r"pscp -scp -i %UserProfile%\.ssh\sitesmash.ppk -r sebodev@webfaction:{} {}".format(plugins_dir, vars.), shell=True)
# print( "copied (if everything went well) {} to {}".format(vars.current_project, vars.project_dir) )
# print("configuring")
