from subprocess import *
import subprocess
import sys

def getPower(host, user="root", password="calvin"):
    cmd = "/usr/local/bin/ipmitool -H " + host + " -U " + user + " -P " + password + " power status"
    p = subprocess.Popen(cmd, stdout=PIPE, shell=True)
    print "getPower(%s) = %s)" % (host, p.stdout.read())

def powerCycle(host, user="root", password="calvin"):
    cmd = "/usr/local/bin/ipmitool -H " + host + " -U " + user + " -P " + password + " power cycle"
    print "CMD: %s" % cmd
    p = subprocess.Popen(cmd, stdout=PIPE, shell=True)
    print "powerCycle(%s) = %s)" % (host, p.stdout.read())

def powerOn(host, user="root", password="calvin"):
    cmd = "/usr/local/bin/ipmitool -H " + host + " -U " + user + " -P " + password + " power on"
    p = subprocess.Popen(cmd, stdout=PIPE, shell=True)
    print "powerCycle(%s) = %s)" % (host, p.stdout.read())

def powerOff(host, user="root", password="calvin"):
    cmd = "/usr/local/bin/ipmitool -H " + host + " -U " + user + " -P " + password + " power off"
    p = subprocess.Popen(cmd, stdout=PIPE, shell=True)
    print "powerCycle(%s) = %s)" % (host, p.stdout.read())
