''' A module of useful variables consisting mainly of variables
created from command line arguments and from data in config files. '''
import configparser
from pathlib import Path

def _get_project_from_dir(the_dir):
    ''' returns which project a directory is inside of '''
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

#create our config readers
sebo_conf = configparser.RawConfigParser()
sebo_conf.read( str(script_dir / 'sebo-utils.conf') )

credentials_conf = configparser.RawConfigParser()
credentials_conf_loc = sebo_conf.get('locations', 'credentials_conf_loc', fallback=None)
if not credentials_conf_loc:
    credentials_conf_loc = storage_dir / "credentials.conf"
google_drive_root_dir = Path( sebo_conf.get('locations', 'google_drive', fallback="") )
google_drive_smash_utils_dir = google_drive_root_dir / "smash-utils"
google_drive_maintenance_dir = google_drive_root_dir / "Sebo Dev" / "WordPress Warranty & Maintanence"

credentials_conf.read( str(credentials_conf_loc) )
#read vars from conf files
ftp_host             = credentials_conf.get('webfaction', 'host', fallback=None)
ssh_username         = credentials_conf.get('webfaction', 'ssh-username', fallback=None)
ssh_password         = credentials_conf.get('webfaction', 'ssh-password', fallback=None)
ftp_username         = credentials_conf.get('webfaction', 'ftp-username', fallback=None) or ssh_username
ftp_password         = credentials_conf.get('webfaction', 'ftp-password', fallback=None) or ssh_password
projects_root_dir    = Path(sebo_conf.get('locations', 'project_dir', fallback=""))
google_drive_client_secret = credentials_conf.get('google-drive', 'client-secret', fallback=None)
lastpass_username = credentials_conf.get('lastpass', 'username', fallback=None)
lastpass_password = credentials_conf.get('lastpass', 'password', fallback=None)

#save some variables from the command line options
from cmd_args import args

current_project     = args.current_project if args.current_project else _get_project_from_dir(".")
theme               = args.theme if args.theme else current_project
md5_passwd          = args.md5 if args.md5 else None

try:
    dns             = args.dns[0]
    dns_output_file = args.dns[1]
except IndexError:
    dns_output_file = None

try:
    wpw_name        = args.wpw[0]
    wpw_level       = int(args.wpw[1])
except IndexError:
    wpw_name = wpw_level = None

verbose             = getattr(args, 'verbose')

change_current_project(current_project)

#the xmlrpc object for communicating with webfaction see https://docs.webfaction.com/xmlrpc-api/tutorial.html#getting-started and https://docs.webfaction.com/xmlrpc-api/apiref.html#method-login
#the session id will automatically be provided
try:
    import xmlrpc.client, functools
    webfaction = xmlrpc.client.ServerProxy("https://api.webfaction.com/")
    wf_id = webfaction.login(ftp_username, ftp_password)[0]
except:
    #ToDo only try to login for commands that require the use of the webfaction api
    pass
