'copies a theme from the webfaction server and readies the environment for dev use'

from __future__ import print_function
import subprocess, os.path
import vars

subprocess.call(r"pscp -scp -i %UserProfile%\.ssh\private_key.ppk -r sebodev@webfaction:{} {}".format(vars.webfaction_theme_dir, vars.project_dir), shell=True)
print( "copied {} to {}".format(vars.current_project, vars.project_dir) )
print("configuring")
import configure_project
