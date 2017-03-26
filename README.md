Overview
--------

Hopefully something to make wordpress junk easier

Configuration file
------------------

The local mysql development database.

Creating a new installation
---------------------------

	autowp create --username t5_admin --url t5.test.lan

This is if you start a completely new project and want to get started. This wraps around two other key tools, wp-cli and wordmove (both of which should be available globally).

The steps:
	- create a new folder in public_html 


Provision a installation
------------------------

This populates a new server 

	autowp provision --local-url t5.test.lan --remote-url t5.co.uk


Delete a local copy
-------------------

For safety reasons, this just deletes the local copy of the database, files and nginx config. Log in to the VPS provider to delete the production copy which is usually a case of deleting the whole vps.

	autowp delete --local-url t5.test.lan
