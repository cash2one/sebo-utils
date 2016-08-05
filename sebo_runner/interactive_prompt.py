import sys

def new(tasks_to_run):
    try:
        ans = input('\nType t and then hit enter if \n' \
                        ' a) This is for a template \n' \
                        ' b) This is for a starter site\n' \
                        ' c) You would like to create a custom site, but you don\'t plan on doing any dev work on the site\n' \
                        'Otherwise, type c \n' \
                        ).lower()[0]
        if ans == 't':
            tasks_to_run.wordpress = True
            print('A Chrome window will open shortly')
        elif ans == 'c':
            ans = input("Do you need to set up the wordpress site for this custom project. Type yes or no").lower()[0]
            if ans == 'y':
                tasks_to_run.wordpress = True
            ans = input("Do you need to create the _s theme. This will create it on both the webfaction server, and on your computer. Type no if the theme already exists on webfaction. Type yes or no").lower()[0]
            if ans == 'y':
                tasks_to_run.new_s_project = True
            else:
                ans = input("In that case the theme must already exist on webfaction, and we just need to copy it to this computer. Type yes or no").lower()[0]
                if ans == 'y':
                    tasks_to_run.existing_s_project = True
                else:
                    print("I give up. I have no idea what you want to do. Type sebo --help for a full list of options")
        else:
            print('Fine, just ignore my instructions of typing t or c. I\'m going to ignore you too')
    except IndexError:
        raise Exception('\n\n  I didn\'t get a valid response from you :( ')


def get_missing_info(args):
    """ if there wasn't enough info passed in on the command line, we ask the user for that info """

    commands_requiring_project_arg = [
        '-_', '--new_s-project',
        "-e", "--existing_s-project",
        "-wp", "--wordpress",
        "-n", "--new"
        ]
    if not set(commands_requiring_project_arg).isdisjoint(sys.argv): #if any value in the list requires_project_arg matches a value in sys.argv
        while not args.current_project:
            args.current_project = str(input('Enter a project (or a subdomain): '))
            sys.argv.append(args.current_project)

    if not set(["--dns"]).isdisjoint(sys.argv):
        while not args.dns:
            args.dns = str(input('Enter a domain (example google.com): '))

    if not set(["--md5", "--hash"]).isdisjoint(sys.argv):
        if not args.md5:
            args.md5 == str(input('Enter a password or leave empty for a random one: '))

    if not set(["--filezilla"]).isdisjoint(sys.argv):
        if not args.filezilla:
            args.filezilla == str(input('Enter the name of a Filezilla entry: '))

    return args
