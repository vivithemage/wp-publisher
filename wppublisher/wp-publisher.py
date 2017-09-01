import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets

import gui

def catch_exceptions(t, val, tb):
    QtWidgets.QMessageBox.critical(None,
                                   "An exception was raised",
                                   "Exception type: {}".format(t))
    old_hook(t, val, tb)

old_hook = sys.excepthook
sys.excepthook = catch_exceptions

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = gui.App()
    sys.exit(app.exec_())
    raise RuntimeError
