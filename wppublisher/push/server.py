import digitalocean

class digital_ocean():
    def __init__(self):
        self.test = 'none';

    def create(self):
        apiKey = "eff3d2d39c9a7cd088a0be8f6d8859361057da4c7f21d5540e0456c9ec3fa726"

        manager = digitalocean.Manager(token=apiKey)
        my_droplets = manager.get_all_droplets()
        print(my_droplets)
        with open('user_data.txt', 'r') as myfile:
            user_data = myfile.read()

        print(user_data)

        droplet = digitalocean.Droplet(token=apiKey,
                                       name='Example1253',
                                       region='nyc2',  # New York 2
                                       image='ubuntu-14-04-x64',  # Ubuntu 14.04 x64
                                       size_slug='512mb',  # 512MB
                                       user_data=user_data)