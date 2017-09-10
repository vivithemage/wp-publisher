import os
import io
import requests
import zipfile
import logging
import pymysql.cursors

class Database:
    def __init__(self, variables):
        self.variables = variables

    def generate_database_name(self):
        site_url = self.variables['site_url']
        site_url_split = site_url.split('.')
        database_name = site_url_split[0]
        return database_name

    def create_database(self):
        # Connect to the database
        print(self.variables)
        connection = pymysql.connect(host=self.variables['database']['hostname'],
                                     user=self.variables['database']['username'],
                                     password=self.variables['database']['password'],
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "create database " + self.generate_database_name()
                cursor.execute(sql)

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

        finally:
            connection.close()

class Wordpress:
    def __init__(self, variables):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        self.wp_url = 'https://wordpress.org/latest.zip'
        self.variables = variables

        self.installation_folder = self.variables['path'] + '/' + self.variables['site_url']
        self.config_file = self.installation_folder + '/wp-config.php'

    def write_config_variables(self, database_name):
        # Read in the file
        with open(self.config_file, 'r') as file:
            filedata = file.read()

        # Replace the database placeholder variables
        filedata = filedata.replace('database_name_here', database_name)
        filedata = filedata.replace('username_here', self.variables['database']['username'])
        filedata = filedata.replace('password_here', self.variables['database']['password'])
        filedata = filedata.replace('localhost', self.variables['database']['hostname'])

        # Write the file out again
        with open(self.config_file, 'w') as file:
            file.write(filedata)

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
        '''
        Create blank database on server
        '''
        db = Database(self.variables)
        db.create_database()
        database_name = db.generate_database_name()

        self.download_and_extract()
        self.change_installation_path()
        self.rename_sample_config()
        self.write_config_variables(database_name)

        self.logger.info('Finished Installation')
