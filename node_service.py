import rpyc
from rpyc.utils.server import ThreadedServer
import datetime
import sys
from node import Node, STATES, CS_TIME_OUT_INTERVAL
import numpy as np
import threading, time
import queue

list_of_nodes = []
nodes_queue = queue.Queue()
critical_section = 'Karabakh is Azerbaijan' # It is just shared resource
class NodeService(rpyc.Service):
    def __init__(self, count_n):
        for id in range(1, count_n+1):
            node = Node(id=id)
            node.setDaemon(True)
            node.start()
            list_of_nodes.append(node)


    def get_time(self):
        return datetime.datetime.now()

    def exposed_recieve_msg(self, id):
        wanted_nodes = []
        if all((node.id != id) & (node.state == STATES.DO_NOT_WANT) for node in list_of_nodes):
            for node in list_of_nodes:
                if (node.id == id) & (node.state == STATES.WANTED):
                    node.state = STATES.HELD
        
        
        for node in list_of_nodes:
            if (node.state == STATES.WANTED) & (node not in wanted_nodes):
                wanted_nodes.append(node)
        
        wanted_nodes.sort(key=lambda x: x.time_stamp, reverse=False)
        nodes_queue = queue.Queue()
        for node in wanted_nodes:
            nodes_queue.put(node)
        n = nodes_queue.get()
        if all(node.state != STATES.HELD for node in list_of_nodes):
            n.state = STATES.HELD
            n.data = critical_section
        
            

        
    def run(self):
        if not nodes_queue.empty():
            n = nodes_queue.get()
            n.state = STATES.HELD
            # time.sleep(CS_TIME_OUT_INTERVAL)


def rpc_main(server):
	server.start()   

if __name__ == '__main__':
    n_count = int(sys.argv[1])
    t = ThreadedServer(NodeService(n_count), port=18888)
    
    rpc_thread = threading.Thread(target=rpc_main, args=(t,), daemon=True)
    rpc_thread.start()
    time.sleep(1)

    while True:
        command = str(input('Input the command - (list, time-p, time-cs, exit): '))

        if command == 'list':
            for node in list_of_nodes:
                print(f'P{node.id}, {node.state.value}')
        if 'time-p' in command:
            t = int(command.split(' ')[1])
            for node in list_of_nodes:
                node.set_time_out_interval(t)

            new_queue = queue.Queue()
            while not nodes_queue.empty():
                n = nodes_queue.get()
                n.set_cs_time_out_interval(t) 
                new_queue.put(n)
        
        if 'time-cs' in command:
            t = int(command.split(' ')[1])
            for node in list_of_nodes:
                node.set_cs_time_out_interval(t) 

            new_queue = queue.Queue()
            while not nodes_queue.empty():
                n = nodes_queue.get()
                n.set_cs_time_out_interval(t) 
                new_queue.put(n)

        if command == 'exit':
            raise SystemExit()
            
        

