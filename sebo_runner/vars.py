''' A module of useful variables consisting mainly of variables
created from command line arguments and from data in config files. '''
import os.path, sys, ConfigParser

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


script_dir = os.path.dirname( os.path.dirname(os.path.realpath(sys.modules[__name__].__file__)) ) # just getting the parent directory of this file

#create our config readers
sebo_conf = ConfigParser.RawConfigParser()
sebo_conf.read( os.path.join(script_dir, 'sebo-utils.conf') )
credentials_conf = ConfigParser.RawConfigParser()
credentials_conf.read( sebo_conf.get('locations', 'credentials_conf_loc') )

#read vars from conf files
ftp_host             = credentials_conf.get('webfaction', 'host')
ftp_username         = credentials_conf.get('webfaction', 'username')
ftp_password         = credentials_conf.get('webfaction', 'password')
projects_root_dir          = sebo_conf.get('locations', 'project_dir')

#save some vars from the command line options
from get_cmd_line_options import args
current_project    = getattr(args, 'current_project', get_project_from_dir(os.getcwd()) )
theme              = getattr(args, 'theme', current_project)

#A few more variables
project_dir          = os.path.join( projects_root_dir, current_project or '' )
webfaction_theme_dir = '/home/%s/webapps/%s/wp-content/theme/%s/' % (ftp_username, current_project, theme)
