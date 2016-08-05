''' parses the command line options, and stores the result in the args variable.
The stored variable name is the same as its command line option except
any - is replaced with a _ and the beginning -'s are removed.
also the project name is stored as the variable current_project '''
import sys, argparse

if len(sys.argv) == 1:
    sys.argv.append('-h')

#we're going to manually handle the current project arg,
#and then let argparse handle the other args.
try:
    if sys.argv[1].startswith('-'):
        if len(sys.argv) >= 3:
            if sys.argv[2].startswith('-'):
                current_project = sys.argv[3] #when running "sebo <command> <command> <projectName>"
            else:
                current_project = sys.argv[2] #when running "sebo <command> <projectName>"
        else:
            current_project = None #when running "sebo <command>"
    else:
        current_project = sys.argv[1] #when running "sebo <projectName> <command>"
except IndexError:
    current_project = None #no project name specified

#prompt the user for the project name if the command being used requires it and it was not provided
requires_project_arg = [
    '-_', '--new_s-project',
    "-e", "--existing_s-project",
    "-wp", "--wordpress",
    "-n", "--new",
    "--dns", "--md5"
    ]
if not set(requires_project_arg).isdisjoint(sys.argv): #if any value in the list requires_project_arg matches a value in sys.argv
    if not current_project:
        if "--dns" in sys.argv:
            current_project = raw_input('Enter a domain (example google.com): ')
        elif "--md5" in sys.argv:
            if "--random" in sys.argv:
                current_project = None
            else:
                current_project = raw_input('Enter a password: ')
        else:
            current_project = raw_input('Enter a project (or a subdomain): ')

#remove current_project from sys.argv so argParse doesn't throw a fit
try:
    sys.argv.remove(current_project)
except ValueError:
    pass #ignore cases where current_project is not in sys.argv


#create our command line options

usage_help_str = '''sebo command projectName [options]
or:    sebo [--update] [--watch]
'''

parser = argparse.ArgumentParser(epilog="More info can be found at http://sebooperations.com/sebo-utils-documentation", usage=usage_help_str, add_help=False)

maintenance = parser.add_argument_group('Maintenance and general purpose utils')
custom = parser.add_argument_group('Utils for Custom Projects')
template = parser.add_argument_group('Utils for Template Projects')
other = parser.add_argument_group('Other options')

custom.add_argument("-_", "--new_s-project", action="store_true", help="Create a new _s project" )
custom.add_argument("-e", "--existing_s-project", action="store_true", help="retrieve an existing _s project")
custom.add_argument("-wp", "--wordpress", action="store_true", help="sets up a new wordpress site")
custom.add_argument("--theme", help="Can be used in conjuction with --existing_s-project if the theme name differs from the project name")
custom.add_argument("-w", "--watch", help="watches the project for changes. This accomplishes the same thing as running the gulp command", action="store_true")

maintenance.add_argument("--dns", nargs="*", help="Saves the dns records into a text file. Pass in a website to lookup and optionally a file to save the results to")
maintenance.add_argument("--md5", help="takes a password and outputs the md5 hash and copies it to the clipboard.", action="store_true")
custom.add_argument("--random", help="Can be used in conjuction with --md5 to create a random password", action="store_true")

other.add_argument("-s", "--serve", help="Starts an http server, allowing other computers to interact with this script", action="store_true")
other.add_argument("-n", "--new", help="Forget the other commands, this one runs through an interactive session to help you set things up.", action="store_true")
other.add_argument("--update", help="updates this script", action="store_true")
#other.add_argument("-v", "--verbose", help="", action="store_true")
other.add_argument("-h", "--help", action="help", help="")

args = parser.parse_args()
#add back in the arg we manually handled
args.current_project = current_project
sys.argv.append(current_project)
