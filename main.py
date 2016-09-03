''' The runner for all of the other scripts '''

import os, sys, subprocess, builtins

#add sebo_runner and lib to the system path
this_dir = os.path.dirname(os.path.realpath(__file__))
runner_dir = os.path.join(this_dir, 'runner')
lib_dir = os.path.join(this_dir, 'lib')
sys.path.append(runner_dir)
sys.path.append(lib_dir)

import vars #oops I just overwrote a built in function. Access it from __builtin__.vars if yous need it.
from get_cmd_line_options import args as tasks_to_run

if tasks_to_run.new:
    import interactive_prompt
    interactive_prompt.new(tasks_to_run)

if tasks_to_run.update:
    subprocess.call( 'cd %s & git pull' % vars.script_dir )

if tasks_to_run.wp:
    import wordpress_utils.wordpress_install

if tasks_to_run.new_s_project:
    import wordpress_utils.new_project

if tasks_to_run.existing_s_project:
    import wordpress_utils.existing_project

if tasks_to_run.watch:
    import wordpress_utils.watch

if tasks_to_run.filezilla:
    import maintenance_utils.filezilla_passwords

if ("--md5" in sys.argv or "--hash" in sys.argv):
    import maintenance_utils.md5

if tasks_to_run.dns: # because of the way this one was read in from the command line, tasks_to_run.dns could be an empty list
    import maintenance_utils.dns

if not any(list(builtins.vars(tasks_to_run).values())[1:]): #if only the project name was passed in
    if not sys.argv[1].startswith('-'):
        print('That\'s a cool project name, but what am I suppose to do with that project.')
