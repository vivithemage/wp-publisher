Overview
--------

This should allow for quicker initial setup and eventual publication of wordpress sites on standalone vps servers.

Installation
------------

TODO

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
