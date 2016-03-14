'copies a theme from the webfaction server and readies the environment for dev use'

from __future__ import print_function

# if we're running this script independent of the framework
# we need to add the sebo_runner directory to the path
if __name__ == "__main__":
    import sys
    this_dir = os.path.dirname(os.path.realpath(__file__))
    script_dir = os.path.dirname(this_dir)
    sebo_runner_dir = os.path.join(script_dir, 'sebo_runner' )

    sys.path.append(sebo_runner_dir)
    print(sebo_runner_dir)
    #main()

import subprocess, os.path
import vars

def main():
    subprocess.call("pscp -i %UserProfile%\.ssh\private_key.ppk -r sebodev@webfaction:%s %s" %(vars.webfaction_theme_dir, vars.project_dir))
    print( "copied %s to %s" % (vars.current_project, vars.project_dir) )
    print("configuring")
    subprocess.call("python configure_project.py", [vars.current_project, vars.project_dir, vars.webfaction_theme_dir])
