
import logging
import os
import inspect
import logging.handlers
import sys

class LoggerManager:
    def __init__(self, name='LoggerManager', console_level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)  # Set the root log level to DEBUG to capture all logs

        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]')

        # Create and configure the console processor
        self.console_handler = logging.StreamHandler(sys.stdout)
        self.console_handler.setLevel(console_level)
        self.console_handler.setFormatter(formatter)

        # Add a processor to the logger
        self.logger.addHandler(self.console_handler)

        # Creating a file processor
        self.file_handler = logging.FileHandler("/root/factorytest.log")
        self.file_handler.setLevel(logging.INFO)
        self.file_handler.setFormatter(formatter)

        self.logger.addHandler(self.file_handler)

    def get_logger(self):
        return self.logger