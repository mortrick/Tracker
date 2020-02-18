import platform
from pathlib import Path
import os.path




# Get session exists run id and return log file

def logpath(runid):
    filename = "processlog1" + str(runid) + ".log"
    if platform.system() == 'Windows':
        logdir = Path('C:/Users/Davidy/Dropbox/Projects/CryptoAPI/logs/')
        path = logdir / filename
        return path
    else:
        logdir = Path('~/cryptoapi/Tracker/logs/')
        path = logdir / filename
        return path


# Get logfile and message

def writelog(logfile, msg,dubugmode =0 ):
    if dubugmode == 0:
        return None
    if os.path.exists(logfile):
        with open(logfile, 'a') as f:
            f.write(msg)
    else:
        f = open(logfile, 'w+')
        f.write(msg)
        f.close()



