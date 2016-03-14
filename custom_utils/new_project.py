''' creates and setups a new _s theme and uploads it to webfaction. '''

from __future__ import print_function
import subprocess, os.path

import paramiko
import vars, ssh


def main():

    webfaction_theme_dir = vars.webfaction_theme_dir
    project_dir = vars.project_dir
    project_name = os.path.dirname(project_dir)

    def assert_webfaction_dir_exists(the_dir):
        transport=paramiko.Transport(vars.ftp_host)
        transport.connect(username=vars.ftp_username,password=vars.ftp_password)
        sftp=paramiko.SFTPClient.from_transport(transport)
        try:
            filestat = sftp.stat(webfaction_theme_dir)
        except IOError:
            pass
        else:
            raise Exception('Whoa, we don\'t want to be overwriting code. The following theme already exists on the webfaction server: ' + webfaction_theme_dir)
    assert_webfaction_dir_exists(webfaction_theme_dir)

    subprocess.call('git clone https://github.com/sebodev/_s project_dir')

    print('\n_s Download complete\nuploading _s to webfaction...')
    #command = 'pscp -i %UserProfile%\.ssh\private_key.ppk -r  %s sebodev@webfaction:%s' % (project_dir, webfaction_theme_dir)
    #subprocess.call(command, cwd=project_dir)
    session=ssh.SSHSession(vars.ftp_host, vars.ftp_username, vars.ftp_password)
    session.put_all(project_dir, webfaction_theme_dir)


    print('Upload complete. Configuring project...')
    subprocess.call('python existing_project.py', [project_name, project_dir, webfaction_theme_dir])
