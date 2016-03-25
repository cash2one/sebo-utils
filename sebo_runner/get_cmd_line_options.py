''' parses the command line options, and stores the result in the args variable.
The stored variable name is the same as its command line option except
any - is replaced with a _ and the beginning -'s are removed.
also the pproject is stored as current_project '''
import sys, argparse



#we're going to manually handle the project arg,
#and then let argparse handle the other args.
if sys.argv[1].startswith('-'):
    if len(sys.argv) >= 3:
        current_project = sys.argv[2] #when running sebo command projectName
    else:
        current_project = None #when running sebo command
else:
    current_project = sys.argv[1] #when running sebo projectName command

#prompt the user for the project name if the command being used requires it and it was not provided
requires_project_arg = [
    '-_', '--new_s-project',
    "-e", "--existing_s-project",
    "-wp", "--wordpress",
    "-n", "--new"
    ]
if not set(requires_project_arg).isdisjoint(sys.argv): #if any value in the list requires_project_arg matches a value in sys.argv
    if not current_project:
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

custom = parser.add_argument_group('Utils for Custom Projects')
template = parser.add_argument_group('Utils for Template Projects')
other = parser.add_argument_group('Other options')

custom.add_argument("-_", "--new_s-project", action="store_true", help="Create a new _s project" )
custom.add_argument("-e", "--existing_s-project", action="store_true", help="retrieve an existing _s project")
custom.add_argument("-wp", "--wordpress", action="store_true", help="sets up a new wordpress site")
custom.add_argument("--theme", help="Can be used in conjuction with --existing_s-project if the theme name differs from the project name" )
custom.add_argument("-w", "--watch", help="watches the project for changes. This accomplishes the same thing as running the gulp command", action="store_true")

other.add_argument("-s", "--serve", help="Starts an http server, allowing other computers to interact with this script", action="store_true")
other.add_argument("-n", "--new", help="Forget the other commands, this one runs through an interactive session to help you set things up.", action="store_true")
other.add_argument("--update", help="updates this script", action="store_true")
#other.add_argument("-v", "--verbose", help="", action="store_true")
other.add_argument("-h", "--help", action="help", help="")

args = parser.parse_args()
#add back in the arg we manually handled
args.current_project = current_project
sys.argv.append(current_project)
