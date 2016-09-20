''' The runner for all of the other scripts '''


import os, sys, subprocess, builtins, argparse
import runner.interactive_prompt

#add sebo_runner and lib to the system path
this_dir = os.path.dirname(os.path.realpath(__file__))
runner_dir = os.path.join(this_dir, 'runner')
lib_dir = os.path.join(this_dir, 'lib')
sys.path.append(runner_dir)
sys.path.append(lib_dir)


usage_help_str = '''sebo command [options]
or for wordpress commands:    sebo command projectName [options]
'''

parser = argparse.ArgumentParser(epilog="More info can be found at http://sitesmash.com/docs/docs/maintenance/other/smash-utils/", usage=usage_help_str, add_help=False)

maintenance = parser.add_argument_group('Maintenance and general purpose')
wordpress = parser.add_argument_group('Wordpress: \nA project name must be specified before using one of these options')
other = parser.add_argument_group('Other options')

other.add_argument("-v", "--verbose", help="displays more verbose/debug info. Also reprompts for credentials, even if these have already been saved", action="store_true")
other.add_argument("-h", "--help", action="help", help="")



tasks = {}

def register(commands):
    """a decorator that registers a commandline option with a function.
    multiple options can be passed in as a list
    If there is a value supplied on the commandline for the option passed in it is provided as an argument to the registered function """
    if isinstance(commands, str):
        commands = [commands]

    def inner(func):

        def command_wrapper():
            for command in commands:
                command = command.lstrip("-")
                command_value = getattr(args, command)
                if command_value:
                    break
            return func(command_value)

        for command in commands:
            tasks[command] = command_wrapper
        return func

    return inner


maintenance.add_argument("--passwords", nargs="?", default="", metavar="search-term", help="Searches Lastpass, Filezilla, and Chrome for passwords")
@register("--passwords")
def passwords(search_term):
    import maintenance_utils.passwords
    if not search_term:
        search_term = input('Enter a search term: ')
    maintenance_utils.passwords.main(search_term)


maintenance.add_argument("--filezilla", nargs="?", default="", metavar="search-term", help="Searches Filezilla for passwords")
@register("--filezilla")
def filezilla(search_term):
    import maintenance_utils.filezilla_passwords
    if not search_term:
        search_term = input('Enter your Filezilla search term: ')
    maintenance_utils.filezilla_passwords.main(search_term)


maintenance.add_argument("--lastpass", nargs="?", default="", metavar="search-term", help="Searches Lastpass for passwords")
@register("--lastpass")
def lastpass(search_term):
    import maintenance_utils.lastpass_passwords
    if not search_term:
        search_term = input('Enter your Lastpass search term: ')
    maintenance_utils.lastpass_passwords.main(search_term)


maintenance.add_argument("--chrome", nargs="?", default="", metavar="search-term", help="Searches Google Chrome for passwords")
@register("--chrome")
def chrome(search_term):
    import maintenance_utils.chrome_passwords
    if not search_term:
        search_term = input('Enter your Chrome search term: ')
    maintenance_utils.chrome_passwords.main(search_term)


other.add_argument("--update", help="updates this script")
@register("--update")
def update(_):
    subprocess.call( 'cd %s & git pull' % vars.script_dir )


wordpress.add_argument("-n", "--new", help="Runs through an interactive session to help you get things setup.")
@register(["-n", "--new"])
def new(_):
    import wordpress_utils.new
    task = wordpress_utils.new.prompt_for_task(tasks_to_run)
    tasks[task]()


#I need to stop saving variables in the vars module for the following

maintenance.add_argument("--dns", nargs="+", default="", const=None, metavar=("domain.com", "output.txt"), help="Does a DNS lookup and optionally saves the results to a text file")
@register("--dns")
def dns(domain):
    import maintenance_utils.dns
    maintenance_utils.dns.main()

maintenance.add_argument("--wpw", nargs="*", default=[], metavar=("client name", "level of warranty (1, 2, or 3)"), help="Performs part of the initial setup for a new WordPress Warranty client. Right now this just sets up a maintenance log in Google Drive.")
@register("--wpw")
def wpw(name):
    import maintenance_utils.wpw_setup

maintenance.add_argument("--md5", nargs="?", default="", metavar="password", help="takes a password and outputs the md5 hash and copies it to the clipboard.")
@register(["--md5, --hash"])
def md5(password):
    import maintenance_utils.md5

wordpress.add_argument("--wp", "--wordpress", action="store_true", help="sets up a new wordpress site")
@register(["--wp", "--wordpress"])
def wp(site_name):
    import wordpress_utils.wordpress_install

wordpress.add_argument("-_", "--new_s-project", action="store_true", help="Create a new _s project" )
@register(["-_", "--new_s-project"])
def new_s_project():
    import wordpress_utils.new_project

wordpress.add_argument("-e", "--existing_s-project", action="store_true", help="retrieve an existing _s project")
wordpress.add_argument("--theme", help="Can be used in conjuction with --existing_s-project if the theme name differs from the project name")
@register(["-e", "--existing_s-project"])
def existing_s_project():
    import wordpress_utils.existing_project

wordpress.add_argument("-w", "--watch", help="watches the project for changes. This accomplishes the same thing as running the gulp command", action="store_true")
@register(["-w", "--watch"])
def watch():
    import wordpress_utils.watch

if len(sys.argv) == 1:
    sys.argv.append('-h')

args, other_args = parser.parse_known_args()

args = runner.interactive_prompt.get_missing_info(args)

import cmd_args
cmd_args.args = args

if other_args:
    args.current_project = other_args.pop(0)
else:
    args.current_project = None

import vars #oops I just overwrote a built in function. To access it use `import builtins; builtins.vars`

for cmd in sys.argv:
    if cmd in tasks:
        tasks[cmd]()

if sys.argv[1] not in tasks.keys():
    raise Exception("Whoops, check your spelling on that one. I don't recognize {}".format(sys.argv[1]))

if other_args:
    raise Exception("recieved extra argument {} {}".format(other_args, sys.argv) )
