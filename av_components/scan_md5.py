import sys
import os
import hashlib

sys.path.append(os.getcwd())
import util as ut

class SCANMD5:
    def __init__(self, f):
        self.file = f
        self.is_virus = False
        self.hash_md5 = ""
        ut.check_verbosity(f"{ut.bcolors.BOLD}---  Starting MD5 Hash  ---{ut.bcolors.ENDC}")
        self.scan_md5()
        ut.check_verbosity(f"{ut.bcolors.BOLD}---  Ending MD5 Hash  ---{ut.bcolors.ENDC}")
        ut.check_verbosity()

    def scan_md5(self):
        ut.check_verbosity(f"{ut.bcolors.OKBLUE}\t*  Starting Hashing{ut.bcolors.ENDC}")
        with open(self.file, "rb") as f:
            bytes = f.read()
            self.hash_md5 = hashlib.md5(bytes).hexdigest()
            ut.check_verbosity(f"{ut.bcolors.OKBLUE}\t*  File hashed, MD5 Hash:{ut.bcolors.ENDC}")
            ut.check_verbosity(f"{ut.bcolors.CYELLOW}\t   >  {self.hash_md5}{ut.bcolors.ENDC}")
            ut.check_verbosity(f"{ut.bcolors.OKBLUE}\t*  Matching Hashes to Find Virus...{ut.bcolors.ENDC}")
            with open(os.path.join(os.getcwd(), "virus-signatures", "md5.txt"),'r') as f:
                    lines = [line.rstrip() for line in f]
                    for line in lines:
                          if str(self.hash_md5) == str(line.split(";")[0]):
                                self.is_virus = True
                    f.close()
            ut.check_verbosity(f"{ut.bcolors.OKBLUE}\t*  Matching Hashes Completed!{ut.bcolors.ENDC}")

    def get_stats(self):    
            if self.is_virus:
                  return {"hash": self.hash_md5, "is_virus": True}
            else:
                  return {"hash": self.hash_md5, "is_virus": False}

if __name__ == "__main__":
      if ut.get_config()["env"] == "test":
            sts = SCANMD5(os.path.join(os.getcwd(), "av_components", "vi.vbs")).get_stats()
            print(sts)