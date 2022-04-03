import rpyc
from rpyc.utils.server import ThreadedServer
import datetime
import time
import threading
import _thread
import socket
import enum, sys
import numpy as np

TIME_OUT_INTERVAL = 5
CS_TIME_OUT_INTERVAL = 10
SERVER = 'localhost'
PORT = 18888

class STATES(enum.Enum):
    DO_NOT_WANT = "DO-NOT-WANT"
    WANTED = "WANTED"
    HELD = "HELD"

class Node(threading.Thread):
    def __init__(self, id):
        threading.Thread.__init__(self)
        global TIME_OUT_INTERVAL
        global CS_TIME_OUT_INTERVAL
        TIME_OUT_INTERVAL = 5
        CS_TIME_OUT_INTERVAL = 10
        self.state = STATES.DO_NOT_WANT
        self.id = id
        self.time_stamp = self.get_timestamp()
        self.data = None
        
    def get_timestamp(self):
        return datetime.datetime.timestamp(datetime.datetime.now())

    def set_time_out_interval(self, time_out):
        global TIME_OUT_INTERVAL
        TIME_OUT_INTERVAL = np.random.randint(5, time_out)

    def set_cs_time_out_interval(self, time_out):
        global CS_TIME_OUT_INTERVAL
        CS_TIME_OUT_INTERVAL = np.random.randint(10, time_out)

    def run(self):
        while True:
            
            if self.state == STATES.DO_NOT_WANT:
                time.sleep(TIME_OUT_INTERVAL)
                self.state = STATES.WANTED
                self.time_stamp = self.get_timestamp()
                self.send_message()
            elif self.state == STATES.WANTED:
                time.sleep(TIME_OUT_INTERVAL)
                self.send_message()
            elif self.state == STATES.HELD:
                time.sleep(CS_TIME_OUT_INTERVAL)
                self.time_stamp = self.get_timestamp()
                self.state = STATES.DO_NOT_WANT
                self.data = None
            

    def send_message(self):
        conn = rpyc.connect(SERVER, PORT)
        conn._config['sync_request_timeout'] = None
        conn.root.recieve_msg(self.id)

    
