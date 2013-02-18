import os
import stat
from kickstarter.models import kssettings

def resultCode(res):
    codes = {
        0: "Failed",
        False: "Failed",
        1: "Passed",
        True: "Passed"
    }
    code = codes[res]
    return code

def dirExists(path):
    try:
        path_exists = os.path.isdir(path)
    except:
        return False
    if path_exists == True:
        return True
    else:
        return False

def dirPerms(path):
    if dirExists(path):
        dperms = os.stat(path)
        res= str(dperms.st_mode & stat.S_IRGRP)
        print "DPERM RESULTS::    %s \n\n" % res
        return False
    else:
        return False

def getPath(kssetting_key):
    print "SEARCHING FOR KSSETTING WITH KEY (%s)" % kssetting_key
    setting = kssettings.objects.get(name__exact=kssetting_key)
    path = setting.setting
    return path

def runChecks(checks):
    results = {}
    for check in checks:
        cmd = check.command.split()
        if cmd[0] == "dir_exists":
            path = getPath(cmd[1])
            results[check.name] = resultCode(dirExists(path))
        elif cmd[0] == "dir_perms":
            path = getPath(cmd[1])
            results[check.name] = resultCode(dirPerms(path))
    return results

