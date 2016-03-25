''' The runner for all of the other scripts '''

from __future__ import print_function
import os, sys, subprocess, __builtin__

#add sebo_runner to the system path
this_dir = os.path.dirname(os.path.realpath(__file__))
sebo_runner_dir = os.path.join(this_dir, 'sebo_runner')
sys.path.append(sebo_runner_dir)

import vars #oops I just overwrote a built in function. Access it from __builtin__.vars if yous need it.
from get_cmd_line_options import args as tasks_to_run

if tasks_to_run.new:
    import interactive_prompt
    interactive_prompt.new(tasks_to_run)

if tasks_to_run.update:
    subprocess.call( 'cd %s & git pull' % vars.script_dir )

if tasks_to_run.wordpress:
    import template_utils.wordpress_install

if tasks_to_run.new_s_project:
    import custom_utils.new_project

if tasks_to_run.existing_s_project:
    import custom_utils.existing_project

if tasks_to_run.watch:
    import custom_utils.watch

if tasks_to_run.serve:
    import serve

if not any(__builtin__.vars(tasks_to_run).values()[1:]): #if only the project name was passed in
    if not sys.argv[1].startswith('-'):
        print('That\'s a cool project name, but what am I suppose to do with that project.')
