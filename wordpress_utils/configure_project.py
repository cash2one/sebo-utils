'''used by new_project and existing_project to configure projects
so that the sebo --watch command will be able to keep the project
in sync with webfaction.
'''

import subprocess, os
import os.path
from runner import vars


from . import ftp_credentials
script = os.path.join(vars.script_dir, 'wordpress_utils', 'gulp_creater.py')
subprocess.call("python %s %s %s" % (script, vars.webfaction_theme_dir, os.path.join(vars.project_dir, 'gulpfile.js')), shell=True)
os.chdir(vars.project_dir)
npm_packages = os.path.join(vars.project_dir, "packages.json")
if (os.path.exists(npm_packages)):
    subprocess.call("npm start", shell=True, cwd=vars.project_dir)
elif vars.verbose:
    print("Could not find the file %s. Skipping the npm installation. If this theme was not based off the undescores theme, this is ok." % npm_packages)
print('-' * 80)
print("\nCreated project %s. Happy coding.\n" % vars.current_project)
