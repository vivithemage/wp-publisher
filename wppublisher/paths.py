import os
from time import time

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(ROOT_DIR, 'config')

# add timestamp to name of log file, to allow for multiple files to coexist without being over-written
LOG_PATH = "/wp_publisher{}.log".format(round(time()))
