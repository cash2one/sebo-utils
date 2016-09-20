''' parses the command line options, and stores the result in the args object.
the project name will be stored under vars.current_project '''

import sys, argparse, interactive_prompt

#create our command line options

usage_help_str = '''sebo command [options]
or for wordpress commands:    sebo command projectName [options]
'''

parser = argparse.ArgumentParser(epilog="More info can be found at http://sitesmash.com/docs/docs/maintenance/other/smash-utils/", usage=usage_help_str, add_help=False)

maintenance = parser.add_argument_group('Maintenance and general purpose')
wordpress = parser.add_argument_group('Wordpress: \nA project name must be specified before using one of these options')
other = parser.add_argument_group('Other options')

wordpress.add_argument("-n", "--new", help="Runs through an interactive session to help you get things setup.", action="store_true")
wordpress.add_argument("-_", "--new_s-project", action="store_true", help="Create a new _s project" )
wordpress.add_argument("-e", "--existing_s-project", action="store_true", help="retrieve an existing _s project")
wordpress.add_argument("--wp", "--wordpress", action="store_true", help="sets up a new wordpress site")
wordpress.add_argument("--theme", help="Can be used in conjuction with --existing_s-project if the theme name differs from the project name")
wordpress.add_argument("-w", "--watch", help="watches the project for changes. This accomplishes the same thing as running the gulp command", action="store_true")

maintenance.add_argument("--dns", nargs="+", default="", const=None, metavar=("domain.com", "output.txt"), help="Does a DNS lookup and optionally saves the results to a text file")
maintenance.add_argument("--md5", nargs="?", default="", metavar="password", help="takes a password and outputs the md5 hash and copies it to the clipboard.")
maintenance.add_argument("--filezilla", nargs="?", default="", metavar="entry", help="Filezilla's interface hides passwords, but if you provide the name from Filezilla's site manager, I'll tell you the password")
maintenance.add_argument("--wpw", nargs="*", default=[], metavar=("client name", "level of warranty (1, 2, or 3)"), help="Performs part of the initial setup for a new WordPress Warranty client. Right now this just sets up a maintenance log in Google Drive.")

other.add_argument("--update", help="updates this script", action="store_true")
other.add_argument("-v", "--verbose", help="", action="store_true")
other.add_argument("-h", "--help", action="help", help="")

if len(sys.argv) == 1:
    sys.argv.append('-h')

args, other_args = parser.parse_known_args()

if other_args:
    args.current_project = other_args.pop(0)
else:
    args.current_project = None

if other_args:
    raise Exception("recieved extra argument %s" % other_args)

args = interactive_prompt.get_missing_info(args)
