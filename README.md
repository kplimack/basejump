Basejump
========
Inventory Management and End to End Provisioning

Installation
============
Basejump can be setup in many ways.  You can clone/fork the repo and simply run it as you would any django app, or you can use the provided chef cookbook.
A fixture is provided to insert some demo data.  The default username/password is admin/admin.
* Standalone
``
git clone git@github.com:kplimack/basejump.git
cd basejump
./manage.py syncdb
./manage.py runserver|run_gunicorn
``
* Chef
Simply add `recipe[basejump]` to your node's run_list.
``
{
  "name":"my_node",
    "run_list": [
        "recipe[basejump]"
     ]
}
``
