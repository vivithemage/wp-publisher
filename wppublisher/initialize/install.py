import os, io, requests, zipfile, logging


class Wordpress:
    def __init__(self, variables):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        self.wp_url = 'https://wordpress.org/latest.zip'
        self.variables = variables

        self.installation_folder = self.variables['path'] + '/' + self.variables['site_url']
        self.config_file = self.installation_folder + '/wp-config.php'

    def create_database(self):
        self.logger.info('Creating database')

    def write_config_variables(self):
        # Read in the file
        with open(self.config_file, 'r') as file:
            filedata = file.read()

        # Replace the database placeholder variables
        filedata = filedata.replace('database_name_here', self.variables['database']['hostname'])
        filedata = filedata.replace('username_here', self.variables['database']['username'])
        filedata = filedata.replace('localhost', self.variables['database']['password'])

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
        self.download_and_extract()
        self.change_installation_path()
        self.rename_sample_config()
        self.write_config_variables()
        self.logger.info('Finished Installation')
