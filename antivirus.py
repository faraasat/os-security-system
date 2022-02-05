from tkinter import *
from tkinter import filedialog
from datetime import datetime
import os

from av_components import scan_sha256
from av_components import scan_md5
from av_components import scan_sha1
import util as ut

ss256 = {}
ssm5 = {}
ss1 = {}
is_virus = False
filename = None
det = dict()

def rmfile():
    os.remove(filename)
    button_remove.config(state = DISABLED)
    ut.check_verbosity(f"{ut.bcolors.OKGREEN}\tFile Removed Successfully!!{ut.bcolors.ENDC}\n")

def comp_hashes(fname):
    return [scan_sha256.SCANSHA256(fname).get_stats(), scan_md5.SCANMD5(fname).get_stats(), scan_sha1.SCANSHA1(fname).get_stats()]

def browseFiles():
    global is_virus
    global filename
    button_remove.config(state = DISABLED)
    fname = filedialog.askopenfilename(initialdir = "/", title = "Select a File",  filetypes = (("Text files",  "*.*"),  ("all files", "*.*"))) 
    ut.check_verbosity(f"{ut.bcolors.OKBLUE}\t*  File Selected is:{ut.bcolors.ENDC}")
    ut.check_verbosity(f"{ut.bcolors.CYELLOW}\t   -   {fname}{ut.bcolors.ENDC}\n")
    filename = fname
    label_virus.configure(text = "Virus: N/A")
    label_sha256.configure(text = "SHA256 Hash: N/A")
    label_md5.configure(text = "MD5 Hash: N/A")
    label_sha1.configure(text = "SHA1 Hash: N/A")
    opened_file.configure(text="Scanning File: " + fname)
    label_status.configure(text="Status: Scanning...")
    res = comp_hashes(fname)
    for i in res:
        if i["is_virus"] == True:
            is_virus = True
    label_sha256.configure(text="SHA256 Hash: " + res[0]["hash"])
    label_md5.configure(text="MD5 Hash: " + res[1]["hash"])
    label_sha1.configure(text="SHA1 Hash: " + res[2]["hash"])
    if is_virus:
        ut.check_verbosity(f"{ut.bcolors.FAIL}\tVirus Found{ut.bcolors.ENDC}\n")
        label_virus.configure(text = "Virus: Found")
        button_remove.config(state = NORMAL)
    else:
        ut.check_verbosity(f"{ut.bcolors.OKGREEN}\tVirus Not Found{ut.bcolors.ENDC}\n")
        label_virus.configure(text = "Virus: Not Found")
    det = {"SHA256": res[0]["hash"], "MD5": res[1]["hash"], "SHA1": res[2]["hash"], "Virus": is_virus}
    is_virus = False
    label_status.configure(text="Status: Idle")
    write_logs(det)

def write_logs(d):
    dt = datetime.now()
    dmy = dt.strftime("%d-%m-%Y")
    shm = dt.strftime("%H:%M:%S")
    logger = ut.logger_dir()
    open(os.path.join(logger, "log.txt"), "w+")
    f = open(os.path.join(logger, "log.txt"), "a")
    f.write(f"Started on {dt.strftime('%Y-%m-%d')} at {dt.strftime('%H:%M:%S')}\n\n")
    for i in d.keys():
        f.write(f"{i} : {d[i]}\n")

ut.check_verbosity(f"{ut.bcolors.BOLD}\t\t\t^^^^^^^^^^^^^ Antivirus App Started ^^^^^^^^^^^^^\n{ut.bcolors.ENDC}")
window = Tk() 
window.title('Antivirus') 
window.geometry("500x610")
window.config(background = "white") 

label_file_explorer = Label(window, text = "Antivirus", font="helvetica 25", width = 100, height = 4, fg = "green", bg = "white", wraplength=450, justify="center")
label_status = Label(window, text = "Status: Idle", font="helvetica 10", width = 100, height = 4, fg = "blue", bg = "white", wraplength=450, justify="center")
opened_file = Label(window, text = "File Opened: N/A", font="helvetica 10", width = 100, height = 4, fg = "blue", bg = "white", wraplength=450, justify="center")
label_sha256 = Label(window, text = "SHA256 Hash: N/A", font="helvetica 10", width = 100, height = 4, fg = "purple", bg = "white", wraplength=450, justify="center")
label_md5 = Label(window, text = "MD5 Hash: N/A", font="helvetica 10", width = 100, height = 4, fg = "purple", bg = "white", wraplength=450, justify="center")
label_sha1 = Label(window, text = "SHA1 Hash: N/A", font="helvetica 10", width = 100, height = 4, fg = "purple", bg = "white", wraplength=450, justify="center")
label_virus = Label(window, text = "Virus: N/A", font="helvetica 12", width = 100, height = 4, fg = "red", bg = "white", wraplength=450, justify="center")

button_explore = Button(window, text = "Browse Files", command = browseFiles)
button_remove = Button(window, text = "Remove File", command = rmfile, state = DISABLED)

label_file_explorer.grid(column = 1, row = 1)
label_file_explorer.place(x=-700, y=0)

opened_file.grid(column = 1, row = 1)
opened_file.place(x=-150, y=110)

label_status.grid(column = 1, row = 1)
label_status.place(x=-150, y=175)

label_sha256.grid(column = 1, row = 1)
label_sha256.place(x=-150, y=240)

label_md5.grid(column = 1, row = 1)
label_md5.place(x=-150, y=310)

label_sha1.grid(column = 1, row = 1)
label_sha1.place(x=-150, y=365)

button_explore.grid(column = 1, row = 2)
button_explore.place(x=210, y=450)

label_virus.grid(column = 1, row = 2)
label_virus.place(x=-205, y=470)

button_remove.grid(column = 1, row = 2)
button_remove.place(x=210, y=550)

window.mainloop()