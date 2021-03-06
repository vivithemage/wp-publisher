# Changelog
All changes to this project since 02/09/2019 should be documented in this file, with the latest ones added to the top.

## 09/09/2019
- made installation process rename root folder to 'public_html', so that a subsequent publish process will work without having to rename the folder

- improved field validation:
-- now for installation as well as publication
-- made validation errors, and any Python exceptions raised by the process, display an alert box to the user, rather than being swallowed or relegated to a hard-to-notice line of text at the bottom of the window

- made the installation section prepopulate the database fields, if the user has appropriate environment variables set

## 04/09/2019
- installed phpMyAdmin, which can be accessed at /phpmyadmin at the root of the domain

- overwrote the SQL file, after uploading to server, to replace localhost:8888 with the provided site URL. Also updated the WP_HOME and WP_SITEURL in wp-config. These changes should ensure the site works straight away after the publisher program is complete and the DNS updated

## 03/09/2019
- echoed out the database password to the Logs tab. Fixed regex issue which sometimes caused the db settings not to be updated in wp-config.

- made a message box pop up when the process is complete, and changed some of the progress text to be more accurate

- changed the log output so that most of it goes to a log file (`wp_publisherXXXXXXXXXX.log`, where the `X`'s are the current timestamp), which is available both on your local machine (in the root installation directory, alongside `public_html`) and on the server in the `/var/log` directory

## 02/09/2019
- used absolute paths to the config directory which holds the user data and the `init.sh` script, allowing the program to be run from any directory without crashing 

- made it so that only the wp-config.php file on the server is updated with the new connection details, the local version remains intact

- various improvements to field validation:
  - validation of URL via a regex, with a helpful explicit message if the user incorrectly includes an initial `www.` or `http(s)://`
  - checks that the installation path given actually exists on the filesystem, and has the required `public_html` and `SQL` subfolders
  - refactoring of the validation code, with a separate method for each field, so that it is easier to extend in future than when it was just a long single `if/elif/else` block