import sys
import os
import hashlib

sys.path.append(os.getcwd())
import util as ut

class SCANSHA256:
    def __init__(self, f):
        self.file = f
        self.is_virus = False
        self.hash_sha256 = ""
        ut.check_verbosity(f"{ut.bcolors.BOLD}---  Starting SHA256 Hash  ---{ut.bcolors.ENDC}")
        self.scan_sha256()
        ut.check_verbosity(f"{ut.bcolors.BOLD}---  Ending SHA256 Hash  ---{ut.bcolors.ENDC}")
        ut.check_verbosity()

    def scan_sha256(self):
        ut.check_verbosity(f"{ut.bcolors.OKBLUE}\t*  Starting Hashing{ut.bcolors.ENDC}")
        with open(self.file, "rb") as f:
            bytes = f.read()
            self.hash_sha256 = hashlib.sha256(bytes).hexdigest();
            ut.check_verbosity(f"{ut.bcolors.OKBLUE}\t*  File hashed, MD5 Hash:{ut.bcolors.ENDC}")
            ut.check_verbosity(f"{ut.bcolors.CYELLOW}\t   >  {self.hash_sha256}{ut.bcolors.ENDC}")
            ut.check_verbosity(f"{ut.bcolors.OKBLUE}\t*  Matching Hashes to Find Virus...{ut.bcolors.ENDC}")
            with open(os.path.join(os.getcwd(), "virus-signatures", "sha256.txt"),'r') as f:
                lines = [line.rstrip() for line in f]
                for line in lines:
                    if str(self.hash_sha256) == str(line.split(";")[0]):
                        self.is_virus = True
                f.close()
            ut.check_verbosity(f"{ut.bcolors.OKBLUE}\t*  Matching Hashes Completed!{ut.bcolors.ENDC}")
            
    def get_stats(self):    
        if self.is_virus:
            return {"hash": self.hash_sha256, "is_virus": True}
        else:
            return {"hash": self.hash_sha256, "is_virus": False}

if __name__ == "__main__":
      if ut.get_config()["env"] == "test":
            sts = SCANSHA256(os.path.join(os.getcwd(), "av_components", "vi.vbs")).get_stats()
            print(sts)