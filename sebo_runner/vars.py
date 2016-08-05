''' A module of useful variables consisting mainly of variables
created from command line arguments and from data in config files. '''
import os.path, sys, configparser

def get_project_from_dir(the_dir):
    ''' returns which project a directory is inside of '''
    if (the_dir is None):
        the_dir = os.getcwd()

    projects = os.listdir(projects_root_dir)
    the_dir = os.path.normpath(the_dir) #remove any trailing slashes

    def inner(the_dir):
        parent_dir_path, tail = os.path.split(the_dir)
        if tail in projects:
            return tail
        if not tail:
            return None
        return inner(parent_dir_path)
    return inner(the_dir)

def change_current_project(project):
    global current_project, project_dir, webfaction_theme_dir
    current_project      = project
    project_dir          = os.path.normpath( os.path.join( projects_root_dir, current_project or '' ) )
    webfaction_theme_dir = '/home/%s/webapps/%s/wp-content/themes/%s/' % (ftp_username, current_project, theme)

script_dir = os.path.dirname( os.path.dirname(os.path.realpath(sys.modules[__name__].__file__)) ) # just getting the parent directory of this file
storage_dir = os.path.join(os.path.expanduser('~'), '.sebo-utils') #store files in here so they do not get committed

#create our config readers
sebo_conf = configparser.RawConfigParser()
sebo_conf.read( os.path.join(script_dir, 'sebo-utils.conf') )

credentials_conf = configparser.RawConfigParser()
conf_loc = sebo_conf.get('locations', 'credentials_conf_loc')
conf_loc = conf_loc if conf_loc else os.path.join(storage_dir, "credentials.conf")
credentials_conf.read( conf_loc )

#read vars from conf files
ftp_host             = credentials_conf.get('webfaction', 'host')
ssh_username         = credentials_conf.get('webfaction', 'ssh-username')
ssh_password         = credentials_conf.get('webfaction', 'ssh-password')
ftp_username         = credentials_conf.get('webfaction', 'ftp-username') or ssh_username
ftp_password         = credentials_conf.get('webfaction', 'ftp-password') or ssh_password
projects_root_dir    = os.path.normpath(sebo_conf.get('locations', 'project_dir'))

#save some vars from the command line options
from get_cmd_line_options import args
current_project     = args.current_project if args.current_project else get_project_from_dir(os.getcwd())
theme               = args.theme if args.theme else current_project
md5_passwd          = args.md5 if args.md5 else None
filezilla_entry     = args.filezilla if args.filezilla else None

try:
    dns             = args.dns[0]
    dns_output_file = args.dns[1]
except IndexError:
    dns_output_file = None
verbose            = getattr(args, 'verbose')

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
