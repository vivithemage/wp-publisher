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


'''
This class is too complicated for what it does. 
Too late at night and too much coffee ;/
'''


class WpConfig:
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path

    def _get_single_variable(self, identifier, line):
        regex = r"define\(\s*'" + identifier + r"'\s*,\s*'(.+?)'\s*"
        database_result = re.search(regex, line, re.IGNORECASE)

        if database_result:
            return database_result.group(1)

    def _set_single_variable(self, key, value, line):
        search_regex = r"define\('" + key + "', '(.+?)'"
        #search_regex = r"define\(\s*'" + identifier + r"'\s*,\s*'(.+?)'\s*"
        replace_regex = "define('" + key + "', '" + value + "'"

        if re.search(search_regex, line):
            return re.sub(search_regex, replace_regex, line)
        else:
            return line

    def _group_replace(self, config_variables, line):
        for key, value in config_variables.items():
            line = self._set_single_variable(key, value, line)

        return line

    def read(self):
        wp_config_variables = ('DB_NAME', 'DB_USER', 'DB_PASSWORD')
        wp_config_results = {}

        with open(self.config_file_path, "r") as file:
            for line in file:
                for wp_variable in wp_config_variables:
                    result = self._get_single_variable(wp_variable, line)

                    if result:
                        wp_config_results[wp_variable] = result

        return wp_config_results

    def write(self, db_name='wp_site_db', db_username='root', db_password='root', db_hostname='localhost'):
        new_config_content = ''

        config_variables = {'DB_NAME': db_name, 'DB_USER': db_username, 'DB_PASSWORD': db_password, 'DB_HOST': db_hostname}

        with open(self.config_file_path) as f:
            for line in f:
                new_config_content = new_config_content + self._group_replace(config_variables, line)

        # Write the file out again
        with open(self.config_file_path, 'w') as file:
            file.write(new_config_content)

        return True


class Wordpress:
    def __init__(self, ui_fields):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        self.wp_url = 'https://wordpress.org/latest.zip'
        self.ui_fields = ui_fields

        self.installation_folder = self.ui_fields['path'] + '/' + self.ui_fields['site_url']
        self.config_file = self.installation_folder + '/wp-config.php'

    def rename_sample_config(self):
        source = self.installation_folder + '/wp-config-sample.php'
        destination = self.config_file

        self.logger.info('renaming ' + source + ' to ' + destination)
        os.rename(source, destination)

    def download_and_extract(self):
        self.logger.info('Starting download: ' + self.ui_fields['path'])

        os.chdir(self.ui_fields['path'])
        r = requests.get(self.wp_url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall()
        self.logger.info('Completed download')

    def change_installation_path(self):
        source = self.ui_fields['path'] + '/wordpress'
        destination = self.installation_folder
        self.logger.info('renaming ' + source + ' to ' + destination)
        os.rename(source, destination)

    def start(self):
        db = Database(self.ui_fields)
        db.create_database()
        database_name = db.generate_database_name()

        self.download_and_extract()
        self.change_installation_path()
        self.rename_sample_config()

        wp_config_path = self.installation_folder + '/wp-config.php'
        wp_config = WpConfig(wp_config_path)
        wp_config.write(db_name=database_name,
                        db_username=self.ui_fields['database']['username'],
                        db_password=self.ui_fields['database']['password'],
                        db_hostname=self.ui_fields['database']['hostname'])

        self.logger.info('Finished Installation')
