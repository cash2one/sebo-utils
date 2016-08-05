import hashlib
from Tkinter import Tk
import vars

if vars.randomPasswd:

    import lib.password_creator
    passwd = lib.password_creator.new(length=10)
    md5Passwd = hashlib.md5(passwd.encode('utf-8')).hexdigest()

    print("password: " + passwd)
    print("md5 hash: " + md5Passwd)

else:
    passwd = vars.current_project

    md5Passwd = hashlib.md5(passwd.encode('utf-8')).hexdigest()

    print(md5Passwd)

#now copy it to the clipboard
r = Tk()
r.withdraw()
r.clipboard_clear()
r.clipboard_append(md5Passwd)
r.destroy()
