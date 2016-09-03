""" Retreives and saves DNS records """
import os, os.path, socket, subprocess
import lib.whois, vars

domain = vars.dns

domain = domain.replace("http://", "").replace("https://", "")
domain = domain.rstrip("/")

if "." not in domain:
    user = os.getenv('username') if os.getenv('username') else "user"
    raise Exception("Hey %s. Could you quickly add a .com or a .whatever to the end of that domain. Thanks" % user)

# decide where we will store the results
if vars.dns_output_file:
    if vars.dns_output_file.endswith(".txt"):
        output_file = vars.dns_output_file
    else:
        output_file = os.path.join(vars.dns_output_file, vars.dns + ".txt")
else:
    #create a folder for the dns records if it doesn't exist
    output_folder = os.path.join(vars.storage_dir, 'dnsRecords')
    try:
        os.makedirs(output_folder)
    except WindowsError:
        pass

    output_file = os.path.join(vars.storage_dir, 'dnsRecords', domain + ".txt")

whois_dict = lib.whois.lookup(domain)

if vars.verbose:
    for k, v in whois_dict.items():
        print(k, v)
    print()
    print("-"*80)
    print()

if output_file:
    cmd = 'nslookup -type=any %s'  % domain
    res = subprocess.check_output( cmd ).decode("utf-8")
    with open(output_file, "w") as f:
        f.write(res)
if vars.verbose:
    cmd = 'nslookup -type=any %s'  % domain
    subprocess.call(cmd)
    print()
    print("-"*80)
    print()

cmd = 'nslookup -type=mx %s'  % domain
res = subprocess.check_output( cmd ).decode("utf-8")
if res.find("mail exchanger") > 0:
    try:
        res = res[res.find("mail exchanger") : ]
        res = res.split("=")[1]
        res = res.strip()
        print("\nEmail Server:", res)
    except ValueError:
        print("\nEmail mx record:\n" + res)

try:
    print("Registrar:", whois_dict["Registrar"])
    print("Name Server:", whois_dict["Name Server"])
except KeyError:
    print("I just can't seem to find the registrar or name server")
try:
    print("IP Adress:", socket.gethostbyname(domain))
except socket.gaierror as err:
    print("I couldn't find the IP address either", err)

try:
    cmd = 'nslookup -type=ptr %s'  % socket.gethostbyname(domain)
    res = subprocess.check_output( cmd ).decode("utf-8")
    res = res[res.find("name") : ]
    _, res = res.split("=")
    res = res.strip()
    print("Web Host Server:", res)
except:
    pass
