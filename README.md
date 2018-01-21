Overview
--------

WP Publisher is a gui application that can help drastically speed up local wordpress installation and deployment of to digitalocean servers.

It does this allowing a user to:

1. Install a fresh installation of wordpress locally.
2. Publish a wordpress website to a new digitalocean server.

If you're working with a WAMP development stack and using a single digitalocean vps for each website you host this will almost certainly help you out! Take a look at the video below.

Installation
------------

TODO

## Supports

Tested and working on Windows 7 and 10.

Publication
-----------

Download all the wordpress files and database you would like to use.
Create the following directories:

blog.example.com/public_html
blog.example.com/SQL

Place the root (so copy and paste everything in the directory with wp-config.php in) into public_html
put the sql file into SQL and make sure the sql file has the exact same name as the database name in wp-config.php

Enter the api key and the hostname and press 'start'.


Requirements
------------

Please note that this currently works with python 3.6 only.

To install dependancies do:

    pip install -r requirements.txt

failing that:

    pip install pyqt5 python-digitalocean paramiko pymysql


## Contribute

There's a lot to do and all contributions are very welcome. Please get in touch if you plan to do some work on the project.

The list below details some areas which could do with some attention.

* Add additional error checking on fields (current error checking is very basic).
* Add error checking to installation path folder (ensure it has public_html and SQL folder)
* Investigate issue with Digitalocean api failing to return data.
* Allow for more customization when installing.
* Push all logging to log window and log file.
* Create a stand alone exe and installer (see http://nuitka.net/ http://www.py2exe.org/)
* Integrate with additional cloud server providers (e.g. Amazon, Bytemark).
* Test on Mac and Linux
* Integrate with wordmove by creating a movefile.yml in the wordpress directory when initializing a new wordpress instance locally (https://github.com/welaika/wordmove)
* General improvements to the UI. Maybe an additional options button for people to fine tune the installation (e.g. specify new packages)
* Currently only supports the the ubuntu lemp digitalocean image. Adding support for other distros would be useful. This was done for speed. It would be 
* Integrate mysql backups. This has been partially done with: 


Development notes
-----------------

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
