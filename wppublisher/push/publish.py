import digitalocean
import logging
import paramiko
import time


class DigitalOcean:
    def __init__(self, variables):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # self.api_key = variables['api_key']
        self.api_key = "20f03956273725fe5a6133e5ebcb93de2ea5c454cd8461881ae6cff96c43d50a"
        #self.site_name = variables['site_name']
        self.installation_path = variables['installation_path']

        self.cloud_init_path = 'user_data.txt'
        self.ssh_init_path = 'init.sh'

        self.ip_address_v4 = None

        with open(self.cloud_init_path, 'r') as cloud_init_file:
            user_data = cloud_init_file.read()

        self.instance = digitalocean.Droplet(token=self.api_key,
                                        name='lemptest',
                                        region='lon1',
                                        image='lemp-16-04',
                                        size_slug='512mb',
                                        user_data=user_data)


    '''
    Never use this on a production account
    Used to destroy all servers before
    '''
    def dev_housekeeping(self):
        manager = digitalocean.Manager(token=self.api_key)
        my_droplets = manager.get_all_droplets()
        for droplet in my_droplets:
            droplet.destroy()

    def replace_ssh_command_variables(self, line):
        return line

    def run_init_commands(self, ssh_client):
        with open(self.ssh_init_path) as f:
            for line in f:
                amended_line = self.replace_ssh_command_variables(line)
                stdin, stdout, stderr = ssh_client.exec_command(amended_line)
                self.logger.info(stdout.readlines())

        ssh_client.close()

    '''
    Once the api returns 'completed', the droplet is up and running
    '''
    def ready(self):
        success_message = 'completed'
        actions = self.instance.get_actions()

        for action in actions:
            action.load()
            if action.status == success_message:
                return True
            else:
                self.logger.info('Current Status: ' + action.status)
                return False

    '''
    Creates the server instance
    '''
    def spin_up(self):
        self.instance.create()
        self.instance.load()
        self.ip_address_v4 = self.instance.ip_address

    '''
    Opens up ssh client and returns client to execute commands
    '''
    def open_ssh_connection(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        for attempt in range(0, 5):
            try:
                client.connect(self.ip_address_v4, port=22, username='root', password='5N73XvQN94UCLQWBkeMe8Nqt',
                               allow_agent=True)
            except paramiko.AuthenticationException:
                self.logger.info("Issue connecting to server over ssh, trying again")
                time.sleep(10)

        return client

    '''
    Additional configuration to prepare the site to host wp
    '''
    def configuration(self):
        grace_period_seconds = 30
        max_check_seconds = 60

        for seconds in range(0, max_check_seconds):
            time.sleep(1)
            if self.ready():
                self.logger.info('Server spin up is complete! Giving %d second grace period.' % grace_period_seconds)
                time.sleep(grace_period_seconds)
                self.logger.info('All set, here we go!')
                break
            else:
                self.logger.info("Server not ready, waiting: %d seconds so far" % (seconds))

        self.logger.info("connecting to " + self.ip_address_v4)

        ssh_client = self.open_ssh_connection()
        self.run_init_commands(ssh_client)

    def initialize(self):
        self.logger.info("Removing old machines")
        self.dev_housekeeping()

        self.logger.info('Starting spin up')
        self.spin_up()

        self.logger.info('Starting server configuration')
        self.configuration()

        self.logger.info('Finished')


