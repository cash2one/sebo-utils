import hashlib
from tkinter import Tk
import vars

if not vars.md5_passwd:
    import lib.password_creator
    passwd = lib.password_creator.new(length=10)
else:
    passwd = vars.md5_passwd

md5Passwd = hashlib.md5(passwd.encode('utf-8')).hexdigest()

print(("password: " + passwd))
print(("password hash: " + md5Passwd))


#copy the hash to the clipboard
r = Tk()
r.withdraw()
r.clipboard_clear()
r.clipboard_append(md5Passwd)
r.destroy()
