import os
import stat
import pwd
import grp
from kickstarter.models import kssettings

def getSetting(kssetting_key):
    setting = kssettings.objects.get(name__exact=kssetting_key)
    return setting

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

def dirPerms(path, mode_octal):
    if dirExists(path):
        mode = int(mode_octal, 8)
        return checkMode(path, mode)
    else:
        return False

def fileExists(path):
    try:
        path_exists = os.path.exists(path)
    except:
        return False
    if path_exists == True:
        return True
    else:
        return False

def fileOwner(path, owner=None, group=None):
    if fileExists(path):
        stat_info = os.stat(path)
        uid = stat_info.st_uid
        gid = stat_info.st_gid
        user_name = pwd.getpwuid(uid)[0]
        group_name = grp.getgrgid(gid)[0]
        print "CHECKING OWNER AND GROUP FOR %s" % path
        print "OWNER: %s\nGROUP: %s\n" % (user_name, group_name)
        print "EXPECTED: %s, %s" % (owner, group)
        if owner is None and group is None:
            return [(user_name,group_name)]
        else:
            retCode = True
            if owner is not None and owner is not user_name:
                retCode = False
            if group is not None and group is not group_name:
                retCode = False
            return retCode
    else:
        return False

def checkMode(file, mode=None):
    if fileExists(file):
        filemode = stat.S_IMODE(os.stat(file).st_mode)
        return filemode == mode
    else:
        return False

def getPath(kssetting_key):
    print "SEARCHING FOR KSSETTING WITH KEY (%s)" % kssetting_key
    setting = getSetting(kssetting_key)
    path = setting.setting
    return path

def runChecks(checks):
    results = {}
    for check in checks:
        cmd = check.command.split()
        if cmd[0] == "dir_exists":
            path = getPath(cmd[1])
            res = dirExists(path) == bool(check.result)
            results[check.name] = resultCode(res)
        elif cmd[0] == "dir_perms":
            path = getPath(cmd[1])
            results[check.name] = resultCode(dirPerms(path, check.result))
        elif cmd[0] == "dir_owner":
            path = getPath(cmd[1])
            setting = getSetting(check.result)
            owner = setting.setting
            results[check.name] = resultCode(fileOwner(path, owner))
        elif cmd[0] == "dir_group":
            path = getPath(cmd[1])
            setting = getSetting(check.result)
            group = setting.setting
            results[check.name] = resultCode(fileOwner(path, None, group))
    return results

