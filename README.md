SafeWater Athens
================

This is the git repository for Safewater Athens project from the Hack for 
Athens 2013. 


Authors: Baron Chandler <baron@baronchandler.com>
         Chris Sparnicht <chris@greenman.us>


*TO BUILD*

1. Install Vagrant
2. Install Virtual Box 
3. cd to the root level of the repo, where Vagrantfile is 
4. don't forget to update the submodules for chef provisioning: git submodule update --init --recursive
5. type _vagrant up_ to build a running system in a self-contained virtual machine
6. Edit /etc/hosts to point 127.0.0.1 to safewater.local host
7. Browse to http://safewater.local:8080/

to see the SafeWater Athens main page.


*IMPORT DATA FROM THE EPA*

1. vagrant ssh
2. . /opt/water/var/bin/activate
3. /opt/water/app/manage.py sdwis --import-pws 
4. /opt/water/app/manage.py sdwis --import-violations


