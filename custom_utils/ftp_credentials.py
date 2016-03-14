'''
creates the .ftpass and and remote_sync.json files
'''

from vars import *

remote_sync_file_contents = """
{
  "uploadOnSave": true,
  "deleteLocal": false,
  "hostname": "web353.webfaction.com",
  "ignore": [
    ".remote-sync.json",
    ".git/**",
    "node_modules",
    "bower_components",
    ".sass-cache",
    ".ftppass"
  ],
  "transport": "scp",
  "target": '""" + theme_dir + """',
  "username": '""" + ftp_username + """',
  "password": '""" + ftp_password + """'
}
"""

with open(project_dir + '\\remote_sync.json', 'w') as f:
    f.write(remote_sync_file_contents)

ftppass_contents = """
{
  "keyMain": {
    "user": '""" + ftp_username + """',
    "pass": '""" + ftp_password + """'
  }
}
"""

with open(project_dir + '\\.ftppass', 'w') as f:
    f.write(ftppass_contents)
