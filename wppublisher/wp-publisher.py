import sys
from PyQt5.QtWidgets import (QMainWindow, QTextEdit,
                             QAction, QFileDialog, QApplication)
from PyQt5.QtGui import QIcon

from wppublisher.ui import gui
#from wppublisher.push import server


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = gui.wp_gui()
    sys.exit(app.exec_())