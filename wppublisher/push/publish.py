import digitalocean
import logging
import paramiko
import time


class Configuration:
    def __init__(self, ipv4_address, ssh_username, ssh_password, vps):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        self.ssh_init_path = 'init.sh'
        self.ipv4_address = ipv4_address
        self.ssh_username = ssh_username
        self.ssh_password = ssh_password

        self.vps_instance = vps

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
    Opens up ssh client and returns client to execute commands
    '''
    def open_ssh_connection(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.logger.info("connecting to " + self.ipv4_address)
        try:
            client.connect(self.ipv4_address, port=22, username=self.ssh_username, password=self.ssh_password,
                           allow_agent=True)
        except paramiko.AuthenticationException:
            self.logger.info("Issue connecting to server over ssh, trying again")

        return client

    '''
    Additional configuration to prepare the site to host wp
    '''
    def start(self):
        grace_period_seconds = 30
        max_check_seconds = 60

        for seconds in range(0, max_check_seconds):
            time.sleep(1)
            if self.vps_instance.ready():
                self.logger.info('Server spin up is complete! Giving %d second grace period.' % grace_period_seconds)
                break
            else:
                self.logger.info("Server not ready, waiting: %d seconds so far" % (seconds))

        self.logger.info('Server spun up, additional %d second ssh grace period: ' % grace_period_seconds)
        time.sleep(grace_period_seconds)

        ssh_client = self.open_ssh_connection()

        self.run_init_commands(ssh_client)


class DigitalOcean:
    def __init__(self, variables):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        self.api_key = "20f03956273725fe5a6133e5ebcb93de2ea5c454cd8461881ae6cff96c43d50a"

        self.username = 'root'
        # TODO have this generate a random password
        self.password = '5N73XvQN94UCLQWBkeMe8Nqt'
        self.ip_address_v4 = None
        self.cloud_init_path = 'user_data.txt'

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

    def initialize(self):
        self.logger.info("Removing old machines")
        self.dev_housekeeping()

        self.logger.info('Starting spin up')
        self.spin_up()
        self.logger.info('Successfully spun up server')

        return self.ip_address_v4, self.username, self.password


