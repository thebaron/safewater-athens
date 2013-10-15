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





*THE CHALLENGE*

From http://hackforathens.org/get-involved/challenges/view-challenges/18-challenges/48-safe-drinking-water-challenge:

Within Clarke and Oconee counties, what are the different Public Water Systems (PWS), the population served by each one, the regulating agency and the contact name and phone number.

Within Clarke and Oconee counties, what are the violations and enforcement actions for the different PWSs.

Create a table linking the above violations with the contaminant definitions, health effects, and sources referenced by the violation itself.

Create documents (.txt, .doc, .docx, or .tex) for all PWSs found to have regulatory violation(s) that:
1. Provide the PWS and violation information
2. Are addressed to the relevant agency/contact for the PWS
3. Are distinct, such that each PWS should have its own analysis and document


*THE DATA*

SDWIS Data Model - Contaminant definitions, health effects, and sources of contamination

SDWIS Geography Search - The Safe Drinking Water Information System (SDWIS) contains information about public water systems and their violations of EPA's drinking water regulations, as reported to EPA by the states

QuickStart Guide from EPA


