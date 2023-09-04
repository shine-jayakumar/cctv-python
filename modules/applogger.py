import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
import os
import sys
# from constants.constants import LOG_PATH

LOG_PATH = 'logs'

class AppLogger:

    def __init__(self, name, stdout=True):

        # ====================================================
        # Setting up logger
        # ====================================================
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        logfname = os.path.join(LOG_PATH, f'cctvlog_{datetime.now().strftime("%Y_%m_%d")}.log')

        formatter = logging.Formatter("[%(asctime)s]:[%(name)s]:[%(funcName)s:%(lineno)s]:[%(levelname)s]:%(message)s")
        file_handler = TimedRotatingFileHandler(logfname, when='midnight')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        if stdout:
            stdout_formatter = logging.Formatter("[*] => %(message)s")
            stdout_handler = logging.StreamHandler(sys.stdout)
            stdout_handler.setFormatter(stdout_formatter)
            self.logger.addHandler(stdout_handler)
    
    def getlogger(self):
        """
        Returns the logger object
        """
        return self.logger
        

