''' The runner for all of the other scripts '''

from __future__ import print_function
import os, sys, subprocess

this_dir = os.path.dirname(os.path.realpath(__file__))
sebo_runner_dir = os.path.join(this_dir, 'sebo_runner')
sys.path.append(sebo_runner_dir)

vars_built_in = vars #oops looks like I'm going to overwrite a built in module. I'll just rename the builtin one
import vars
from get_cmd_line_options import args as tasks_to_run

if tasks_to_run.new:
    try:
        ans = raw_input('\nType t and then hit enter if \n' \
                        ' a) This is for a template \n' \
                        ' b) This is for a starter site\n' \
                        ' c) You would like to create a custom site, but you don\'t plan on doing any dev work on the site\n' \
                        'Otherwise, type c \n' \
                        ).lower()[0]
        if ans == 't':
            tasks_to_run.wordpress = True
            print('A Chrome window will open shortly')
        elif ans == 'c':
            ans = raw_input("Do you need to set up the wordpress site for this custom project. Type yes or no").lower()[0]
            if ans == 'y':
                tasks_to_run.wordpress = True
            ans = raw_input("Do you need to create the _s theme. This will create it on both the webfaction server, and on your computer. Type no if the theme already exists on webfaction. Type yes or no").lower()[0]
            if ans == 'y':
                tasks_to_run.new_s_project = True
            else:
                ans = raw_input("In that case the theme must already exist on webfaction, and we just need to copy it to this computer. Type yes or no").lower()[0]
                if ans == 'y':
                    tasks_to_run.existing_s_project = True
                else:
                    print("I give up. I have no idea what you want to do. Type sebo --help for a full list of options.")
        else:
            print('Fine, just ignore my instructions of typing t or c. I\'m going to ignore you too')
    except IndexError:
        raise Exception('\n\n  I didn\'t get a response from you :( ')

if tasks_to_run.update:
    subprocess.call( 'cd %s & git pull' % vars.script_dir )

if tasks_to_run.wordpress:
    #import custom_utils.new_project
    #custom_utils.new_project.main()
    script_path = os.path.join(vars.script_dir, 'template_utils', 'wordpress_install.py')
    args = '  %s' % vars.current_project
    subprocess.call( 'python ' + script_path + args)

if tasks_to_run.new_s_project:
    import custom_utils.new_project
    custom_utils.new_project.main()
    #script_path = os.path.join(vars.script_dir, 'custom_utils', 'new_project.py')
    #args = ' %s %s' % (vars.webfaction_theme_dir, vars.projects_root_dir)
    #subprocess.call( 'python ' + script_path + args, shell=True)

if tasks_to_run.existing_s_project:
    from custom_utils import existing_project
    existing_project.main()

if tasks_to_run.watch:
    if not vars.current_project:
        vars.current_project = raw_input('Enter a project to watch: ')
        vars.project_dir = os.path.join(vars.projects_root_dir, vars.current_project)
    try:
        os.chdir(vars.project_dir)
        print('watching %s' % vars.project_dir)
        subprocess.Popen('gulp < nul', cwd=vars.project_dir, shell=True)
    except WindowsError:
        print("Sorry, I couldn't find any gulp files at", vars.project_dir)

if not any(vars_built_in(tasks_to_run).values()[1:]): #if only the project name was passed in
    print('That\'s a cool project name, but what am I suppose to do with that project.')
