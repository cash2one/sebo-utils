'''used by new_project and existing_project to configure projects
so that the sebo --watch command will be able to keep the project
in sync with webfaction.
'''
from __future__ import print_function
import subprocess, os
import vars


import ftp_credentials
script = os.path.join(vars.script_dir, 'custom_utils', 'gulp_creater.py')
subprocess.call("python %s %s %s" % (script, vars.webfaction_theme_dir, os.path.join(vars.project_dir, 'gulpfile.js')), shell=True)
os.chdir(vars.project_dir)
subprocess.call("npm start", shell=True, cwd=vars.project_dir)
print("\nCreated project %s. Happy coding.\n" % vars.current_project)
