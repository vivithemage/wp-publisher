import sys
from PyQt5.QtWidgets import QApplication

from ui import gui

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = gui.App()
    sys.exit(app.exec_())