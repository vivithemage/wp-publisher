Overview
--------

Hopefully something to make wordpress junk easier

Configuration file
------------------

pyuic5.exe -x .\front_end_design.ui -o front_end.py

The local mysql development database.
Setting up ssh keys
-------------------

* First install puttygen and pageant
* generate a key
* save them both somewhere e.g. c:\ssh_keys
* add the private key to pageant
* Add the public key to wp-publisher


Creating a new installation
---------------------------

	wp-publisher create --username t5_admin --url t5.test.lan

This is if you start a completely new project and want to get started. This wraps around two other key tools, wp-cli and wordmove (both of which should be available globally).

The steps:
	- create a new folder in public_html 


Provision a installation
------------------------

This populates a new server 

	wp-publisher provision --local-url t5.test.lan --remote-url t5.co.uk


Delete a local copy
-------------------

For safety reasons, this just deletes the local copy of the database, files and nginx config. Log in to the VPS provider to delete the production copy which is usually a case of deleting the whole vps.

	wp-publisher delete --local-url t5.test.lan
