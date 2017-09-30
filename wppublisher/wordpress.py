import os
import io
import requests
import zipfile
import logging
import re

from database import Database


'''
Write Method
------------
Goes through every line in the config file and checks if each line 
has any of the variables specified in wp_config_variables.

The always takes the last variable declared in the file which is the
same way the file is processed by the php interpreter. 

Read Method
-----------    
Only writes to a fresh config.
TODO Change this function so it works based on regular expressions instead
'''


class WpConfig:
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path

    def _get_single_variable(self, identifier, line):
        regex = "define\('" + identifier + "', '(.+?)'"
        database_result = re.search(regex, line, re.IGNORECASE)

        '''
        try:
            print (database_result.group(1))
        except:
            print ('')
        '''

        if database_result:
            return database_result.group(1)


    def read(self, wp_config_path):
        wp_config_variables = ('DB_NAME', 'DB_USER', 'DB_USER', 'DB_PASSWORD')
        wp_config_results = {}

        file = open(wp_config_path, "r")

        for line in file:
            for wp_variable in wp_config_variables:
                result = self._get_single_variable(wp_variable, line)

                if result:
                    wp_config_results[wp_variable] = result

        return wp_config_results


    def write(self, db_name='wp_site_db', db_username='root', db_password='root',
              db_hostname='localhost'):
        # Read in the file
        with open(self.config_file_path, 'r') as file:
            filedata = file.read()

        # Replace the database placeholder variables
        filedata = filedata.replace('database_name_here', db_name)
        filedata = filedata.replace('username_here', db_username)
        filedata = filedata.replace('password_here', db_password)
        filedata = filedata.replace('localhost', db_hostname)

        # Write the file out again
        with open(self.config_file_path, 'w') as file:
            file.write(filedata)


class Wordpress:
    def __init__(self, variables):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        self.wp_url = 'https://wordpress.org/latest.zip'
        self.variables = variables

        self.installation_folder = self.variables['path'] + '/' + self.variables['site_url']
        self.config_file = self.installation_folder + '/wp-config.php'

    def rename_sample_config(self):
        source = self.installation_folder + '/wp-config-sample.php'
        destination = self.config_file

        self.logger.info('renaming ' + source + ' to ' + destination)
        os.rename(source, destination)

    def download_and_extract(self):
        self.logger.info('Starting download: ' + self.variables['path'])

        os.chdir(self.variables['path'])
        r = requests.get(self.wp_url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall()
        self.logger.info('Completed download')

    def change_installation_path(self):
        source = self.variables['path'] + '/wordpress'
        destination = self.installation_folder
        self.logger.info('renaming ' + source + ' to ' + destination)
        os.rename(source, destination)

    def start(self):
        db = Database(self.variables)
        db.create_database()
        database_name = db.generate_database_name()

        self.download_and_extract()
        self.change_installation_path()
        self.rename_sample_config()

        wp_config_path = self.installation_folder + '/wp-config.php'
        wp_config = WpConfig(wp_config_path)
        wp_config.write(db_name=database_name,
                        db_username=self.variables['database']['username'],
                        db_password=self.variables['database']['password'],
                        db_hostname=self.variables['database']['hostname'])

        self.logger.info('Finished Installation')
