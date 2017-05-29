import sys
import digitalocean
import paramiko

from PyQt5 import QtCore, QtGui, QtWidgets

from wppublisher.ui import front_end

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window_dialog = QtWidgets.QDialog()
    ui = front_end.Ui_main_window_dialog()
    ui.setupUi(main_window_dialog)
    main_window_dialog.show()
    sys.exit(app.exec_())

    apiKey = "eff3d2d39c9a7cd088a0be8f6d8859361057da4c7f21d5540e0456c9ec3fa726"

    manager = digitalocean.Manager(token = apiKey)
    my_droplets = manager.get_all_droplets()
    print(my_droplets)
    with open('user_data.txt', 'r') as myfile:
        user_data=myfile.read()

    print(user_data)


    droplet = digitalocean.Droplet(token=apiKey,
                                   name='Example1253',
                                   region='nyc2', # New York 2
                                   image='ubuntu-14-04-x64', # Ubuntu 14.04 x64
                                   size_slug='512mb',  # 512MB
                                   user_data=user_data)


    #droplet.create()

    #client = paramiko.SSHClient()
    #client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #client.connect('162.243.17.149', username='demo', allow_agent=True)
    #stdin, stdout, stderr = client.exec_command('ls /')
    #print(stdout.readlines())
    #sys.exit(app.exec_())
