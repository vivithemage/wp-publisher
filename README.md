Overview
--------

Hopefully something to make wordpress junk easier

Please note that this currently works with python 3.6 only.

Generating the GUI
------------------

The gui is created in qt creator using the deisnger feature. This is then saved and converted into a
python class by running the following command:

    pyuic5.exe -x .\front_end_design.ui -o front_end.py

Compiling into standalone application
--------------------------------------

* Make sure mingw is installed along with the gcc package.
* Set the environment variables for the gcc compiler

    $env:CC = "C:\MinGW\bin\mingw32-gcc.exe"

* Run nuitka (install using pip install nuitka)

    nuitka --recurse-all .\wp-publisher.py --standalone --plugin-enable=qt-plugins

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
