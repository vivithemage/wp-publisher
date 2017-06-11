import sys
from PyQt5.QtWidgets import QApplication

from wppublisher.ui import gui

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = gui.wp_gui()
    sys.exit(app.exec_())