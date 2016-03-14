'''used by new_project and existing_project to configure projects
so that the sebo --watch command will be able to keep the project
in sync with webfaction.

arg1: project_name
arg2: project_dir -- this is the full path including the project_name
arg3: webfaction_theme_dir -- the theme's directory on the webfaction server
'''

import subprocess, os.path
import vars


subprocess.call("python ftp_credentials.py %s %s" % (vars.current_project, vars.webfaction_theme_dir)
subprocess.call("python gulp_creater.py %s %s" % (vars.webfaction_theme_dir os.path.join(vars.project_dir, 'gulpfile.js'))
subprocess.call("npm start")
print("\nCreated project %s. Happy coding.\n" % current_project)
