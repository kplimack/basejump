Basejump
========
Inventory Management and End to End Provisioning.
Basejump is written entirely in python.

Installation
============
Basejump can be setup in many ways.  You can clone/fork the repo and simply run it as you would any django app, or you can use the provided chef cookbook.
A fixture is provided to insert some demo data.  The default username/password is admin/admin.
* Standalone
```bash
git clone git@github.com:kplimack/basejump.git
cd basejump
./manage.py syncdb
./manage.py runserver|run_gunicorn
```
* Chef
Simply add `recipe[basejump]` to your node's run_list.
```json
{
  "name":"my_node",
    "run_list": [
        "recipe[basejump]"
     ]
}
```

Requirements
============
* `Centos` >= 5
* `Debian` >= 6

#### packages
- `mysql` - inventory database (could easily swap in any other database you like)
- `tftpd` - tftp server for kicking hosts
- `xinetd` - run tftp server via xinetd
- `syslinux` - syslinux

#### optional packages
- `apache` - frontend to proxy for gunicorn, since gunicorn ain't so good at it
- `nginx` - frontend to proxy, same as apache, but lighter and probably more apt
- `supervisord` - controls gunicorn processes
- `gunicorn` - python application server

Debugging
=========
The best way to debug basejump is to run it manually (not via supervisord/gunicorn).  You will get more debugging output than gunicorn logs.  You can also check the logs, which go to `/var/log/supervisor/basejump-std{out,err}`.  When basejump gets a request for a preseed or kickstart file, it will log the incoming request and response to `$BASEJUMP_PATH/kicker.log`.

Running basejump in debug mode (chef deployed)
----------------------------------------------
```bash
cd /data/www/basejump/
source ./shared/env/bin/activate
cd current
pip install -r requirements.txt
./manage runserver 0.0.0.0:8080
```

Running basejump in debug mode (standalone)
----------------------------------------------
```bash
cd /data/www/basejump/
source ./env/bin/activate
pip install -r requirements.txt
./manage runserver 0.0.0.0:8080
```

Caveats
=======
While testing Debian systems, I noticed that I was unable to get the host to send it's MAC address along with the preseed file request.  RHEL has an option called `kssendmac` and Debian is supposed to have something called `IPAPPEND` (it's in the syslinux docs), but it doesn't work.  So we (Andrew Stone) and I rolled our own `initrd.gz` which sets the client MAC in the `USER_AGENT` header of the request.  You can create your own initrd.gz using the makefile and patch file here [https://github.com/kplimack/debian-initrd].
