''' A module of useful variables consisting mainly of variables
created from command line arguments and from data in config files. '''
import configparser, sys
from pathlib import Path

def _get_project_from_dir(the_dir):
    ''' returns which project a directory is inside of '''
    if not projects_root_dir:
        return None
    try:
        return Path(the_dir).resolve().relative_to(projects_root_dir).parent
    except ValueError:
        return None

def change_current_project(project):
    '''changes the current_project variable along with all variables in this module that are based off of the current_project '''
    global current_project, project_dir, webfaction_theme_dir, theme
    current_project      = project
    project_dir          = projects_root_dir / (current_project or '')
    if theme != current_project:
        project_dir = project_dir / theme
    project_dir = str(project_dir)
    webfaction_theme_dir = '/home/%s/webapps/%s/wp-content/themes/%s/' % (ftp_username, current_project, theme)

script_dir = Path(Path(__file__).resolve().parent.parent) # just getting the parent directory of this file
storage_dir = Path.home() / '.smash-utils' #store files in here that you do not want to have committed like the user credentials config
conf_dir = storage_dir / "confs"

if not conf_dir.is_dir():
    conf_dir.mkdir()

#create our config readers

credentials_conf = configparser.RawConfigParser()
credentials_conf_loc = conf_dir / "credentials.conf"
credentials_conf.read(str(credentials_conf_loc))

webfaction_conf = configparser.RawConfigParser()
webfaction_conf_loc = conf_dir / "webfaction.conf"
webfaction_conf.read(str(webfaction_conf_loc))

google_drive_client_secret = credentials_conf.get('google-drive', 'client-secret', fallback=None)

#I will be removing these as soon as I can, as soon as I switch over to the webfactions dictionary
ftp_host             = credentials_conf.get('webfaction', 'host', fallback=None)
ssh_username         = credentials_conf.get('webfaction', 'ssh-username', fallback=None)
ssh_password         = credentials_conf.get('webfaction', 'ssh-password', fallback=None)
ftp_username         = credentials_conf.get('webfaction', 'ftp-username', fallback=None) or ssh_username
ftp_password         = credentials_conf.get('webfaction', 'ftp-password', fallback=None) or ssh_password

webfaction = {}
def save_webfaction_conf_entries():
    """saves the data in webfaction_conf to the webfaction data"""
    for section in webfaction_conf.sections():
        webfaction[section] = {}
        for (key, val) in webfaction_conf.items(section):
            webfaction[section][key] = val
save_webfaction_conf_entries()
#import pprint; pprint.pprint(webfaction)

sebo_conf = sebo_conf_loc = projects_root_dir = google_drive_client_secret = installed = None
google_drive_root_dir = google_drive_smash_utils_dir = google_drive_maintenance_dir = None
def save_sebo_conf_vars():
    global sebo_conf, sebo_conf_loc, projects_root_dir, storage_dir, installed
    global google_drive_smash_utils_dir, google_drive_maintenance_dir, google_drive_client_secret, google_drive_root_dir

    #read in sebo_conf
    sebo_conf = configparser.RawConfigParser()
    sebo_conf_loc = script_dir / 'sebo-utils.conf'
    sebo_conf.read(str(sebo_conf_loc))

    #save some vars from the conf file
    projects_root_dir = Path(sebo_conf.get('locations', 'project_dir', fallback=""))
    installed = Path(sebo_conf.get('setup_info', 'setup_run', fallback=""))

    #save google drive folders
    google_drive_root_dir = Path( sebo_conf.get('locations', 'google_drive', fallback="") )
    google_drive_smash_utils_dir = google_drive_root_dir / "smash-utils"
    google_drive_maintenance_dir = google_drive_root_dir / "Sebo Dev" / "WordPress Warranty & Maintanence"

    saved_storage_dir = sebo_conf.get('locations', 'stored_data', fallback=None)
    if saved_storage_dir:
        storage_dir = saved_storage_dir

save_sebo_conf_vars()

#save some variables from the command line options
from runner.get_cmd_line_options import args

current_project     = args.current_project if args.current_project else _get_project_from_dir(".")
theme               = args.theme if args.theme else current_project
verbose             = args.verbose

if current_project:
    change_current_project(current_project)
