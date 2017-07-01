import digitalocean
import paramiko
import time


class DigitalOcean:
    def __init__(self, variables):
        # TODO pull this in from settings in gui and pass through
        self.api_key = "20f03956273725fe5a6133e5ebcb93de2ea5c454cd8461881ae6cff96c43d50a"
        self.ip_address_v4 = None
        self.cloud_init_path = 'user_data.txt'

        with open(self.cloud_init_path, 'r') as myfile:
            user_data = myfile.read()

        self.instance = digitalocean.Droplet(token=self.api_key,
                                        name='lemptest',
                                        region='lon1',
                                        image='lemp-16-04',
                                        size_slug='512mb',
                                        user_data=user_data)

        #self.api_key = variables['api_key']

    def dev_housekeeping(self):
        manager = digitalocean.Manager(token=self.api_key)
        my_droplets = manager.get_all_droplets()
        for droplet in my_droplets:
            droplet.destroy()

    # Once it shows 'completed', droplet is up and running
    def ready(self):
        actions = self.instance.get_actions()
        for action in actions:
            action.load()
            if action.status == 'completed':
                return True
            else:
                print('Current Status: ' + action.status)
                return False


    '''
    Creates the server instance
    '''
    def spin_up(self):
        self.instance.create()
        self.instance.load()
        self.ip_address_v4 = self.instance.ip_address

    '''
    Additional configuration to prepare the site to host wp
    '''
    def configuration(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        '''
        Check if the status of the server every second for 50 seconds
        to see if it's ready.
        '''
        grace_period_seconds = 30
        for seconds in range(0, 60):
            time.sleep(1)
            if self.ready():
                print('Server spin up is complete! Giving %d second grace period.' % grace_period_seconds)
                time.sleep(grace_period_seconds)
                print('All set, here we go!')
                break
            else:
                print("Server not ready, waiting: %d seconds so far" % (seconds))

        print("connecting to " + self.ip_address_v4)

        try:
            client.connect(self.ip_address_v4, port=22, username='root', password='5N73XvQN94UCLQWBkeMe8Nqt', allow_agent=True)
        except paramiko.AuthenticationException:
            print("error")

        stdin, stdout, stderr = client.exec_command('ls /')

        print(stdout.readlines())

        client.close()


    def initialize(self):
        print("removing old machines")
        self.dev_housekeeping()
        print('starting spin up')
        self.spin_up()
        print('starting server configuration')
        self.configuration()
        print('finished')


