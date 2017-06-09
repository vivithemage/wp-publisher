import sys
import paramiko

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication
from PyQt5.QtCore import QCoreApplication

from wppublisher.ui import gui
from wppublisher.push import server

def b1_clicked():
   print ("Button 1 clicked")

def selectFile():
    fileDialog = QtGui.QFileDialog()
    fileDialog.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = gui.Ui_MainWindow()
    ui.setupUi(main_window)

    vps = server.digital_ocean()
    # vps.create()

    # ui.publish_start.clicked(ui.get(), b1_clicked)

    # QtCore.QObject.connect(main_window_dialog, QtCore.SIGNAL("installation_start_button"), b1_clicked)

    start_button = ui.installation_start_button
    start_button.clicked.connect(b1_clicked)

    initialize_file_selector = ui.installation_path_file_selector
    initialize_file_selector.clicked.connect(selectFile)

    main_window.show()
    sys.exit(app.exec_())
    # droplet.create()

    # client = paramiko.SSHClient()
    # client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # client.connect('162.243.17.149', username='demo', allow_agent=True)
    # stdin, stdout, stderr = client.exec_command('ls /')
    # print(stdout.readlines())
    # sys.exit(app.exec_())


if __name__ == "__main__":
    main()