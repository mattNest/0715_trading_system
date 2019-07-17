# -*- coding: utf-8 -*-
"""
Created on Tue May  7 15:29:45 2019

@author: neal8
"""
import os
import configparser
import logging
import time
import datetime
import pytz

from bincentive_trader.client import TraderClient

py_path = os.path.dirname(__file__)

config = configparser.ConfigParser()

config.read(py_path + '\MC_Order_Config.ini')
email = config.get('Account_Info', 'email')
password = config.get('Account_Info', 'password')
filename = config.get('File_Path', 'filename')
log_path = config.get('File_Path', 'log_path')
module_path = config.get('File_Path', 'module_path')

logging.basicConfig(level=logging.DEBUG, filename = log_path, format='%(asctime)s - %(levelname)s : %(message)s')

logging.info('Config=> email : '+ email + ' | password : ' + password + ' | filename : ' + filename + ' | log_path : ' + log_path)

def check_signal(sleep_time):
    try:
        while True:
            logging.info('Code running!')
            time.sleep(sleep_time)
            
    except Exception as e:
        logging.error('ERROR! '+ str(e))        
        
check_signal(10)