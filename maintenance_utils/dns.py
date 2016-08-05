""" Retreives and saves DNS records """
import os, os.path, vars, subprocess

domain = vars.current_project

domain = domain.lstrip("http://").lstrip("https://")
domain = domain.rstrip("/")

if "." not in domain:
    user = os.getenv('username') if os.getenv('username') else "user"
    raise Exception("Hey %s. Could you quickly add a .com or a .whatever to the end of that domain. Thanks" % user)

# decide where we will store the results
if vars.dns_output_file:
    if vars.dns_output_file.endswith(".txt"):
        output_file = vars.dns_output_file
    else:
        output_file = os.path.join(vars.dns_output_file, vars.current_project + ".txt")
else:
    #create a folder for the dns records if it doesn't exist
    output_folder = os.path.join(vars.storage_dir, 'dnsRecords')
    try:
        os.makedirs(output_folder)
    except WindowsError:
        pass

    output_file = os.path.join(vars.storage_dir, 'dnsRecords', vars.current_project + ".txt")

# It wouldn't create the output file when I tried to do it this way :( but it does work if I have use a .batch file :)
# args = domain + ' ' + output_file
# cmd = 'nslookup -type=any %s > %s'  % (domain, output_file)
# subprocess.call( cmd )
# cmd = 'nslookup -type=any %s'  % domain
# subprocess.call( cmd )

#run the nslookup command
args = domain + ' ' + output_file
if os.name == 'nt':
    subprocess.call( os.path.join(vars.script_dir, 'maintenance_utils', 'dns.bat ') + args )
else:
    subprocess.call( os.path.join(vars.script_dir, 'maintenance_utils', 'dns.sh ') + args )
