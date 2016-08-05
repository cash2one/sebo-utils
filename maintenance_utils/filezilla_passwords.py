import base64
import lxml.etree
import vars

file = r"C:\Users\Russell\AppData\Roaming\FileZilla\sitemanager.xml"

root = lxml.etree.parse(file)
entry = vars.filezilla_entry.strip()
e = root.xpath('.//Server[text()="' + entry + '"]')
#e = root.xpath('.//Server[contains(text(), "'+ entry +'")]')

host = e[0].find("Host").text
user = e[0].find("User").text
passwd = e[0].find("Pass").text
name = e[0].find("Name").text
encoding = e[0].find("EncodingType").text.lower()
if encoding != "auto" and encoding != "base64":
    raise Exception("Sorry, the password was encrypted using the encryption method '%s' which I do not yet understand how to work with" % encoding)

passwd = base64.b64decode(passwd).decode("utf-8") 

print("\nInfo for", name)
print("host:", host)
print("user:", user)
print("password:", passwd)
