import digitalocean
import paramiko

class digital_ocean():
    def __init__(self):
        self.api_key = "eff3d2d39c9a7cd088a0be8f6d8859361057da4c7f21d5540e0456c9ec3fa726"

    '''
    Creates the server instance
    '''
    def spin_up(self):
        manager = digitalocean.Manager(token=self.api_key)
        my_droplets = manager.get_all_droplets()
        print(my_droplets)
        with open('user_data.txt', 'r') as myfile:
            user_data = myfile.read()

        print(user_data)

        instance = digitalocean.Droplet(token=self.api_key,
                                       name='Example1253',
                                       region='nyc2',  # New York 2
                                       image='ubuntu-14-04-x64',  # Ubuntu 14.04 x64
                                       size_slug='512mb',  # 512MB
                                       user_data=user_data)

        instance.create()

    '''
    Additional configuration to prepare the site to host wp
    '''
    def configuration(self):
        self.spin_up()

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect('162.243.17.149', username='demo', allow_agent=True)
        stdin, stdout, stderr = client.exec_command('ls /')
        print(stdout.readlines())

    def initialize(self):
        self.configuration()

