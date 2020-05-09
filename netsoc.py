import socket
import pickle
import os
import time


class netsoc:
    '''netsoc class
    Wrapper for socket module for 
    easy transmission of python objects

    USAGE
    -----
    create an object by:
    [some var] = netsoc(role of app,[target])

    Example:
    ns = netsoc('client',target=('127.0.0.1',8000)) - for client application
    nss = netsoc('server',target=('127.0.0.1',8000)) - for server application

    ATTRIBUTES
    ----------
    self.role - Role of netsoc object [server/client]
    self.target - Address of server (default - locallost:8000)
    self.soc - socket object
    self.localhost - localhost
    self.client - client connection for server and self.soc for client

    METHODS
    -------
    [netsoc object].send([object]) - send python object to other node
    [netsoc object].recv() - recieve object from other node

    DEPENDENCIES - os,socket,time,pickle
    '''
    
    def __init__(self,role,target=('localhost',8000)):
        '''Constructor for netsoc class'''
        self.role = role
        self.target = target
        self.soc = self._getsoc()
        self.localhost = socket.gethostname()
        if self.role == 'client':
            self._client()
            self.client = self.soc
        elif self.role == 'server':
            self._server()
        
    def _getsoc(self):
        '''Private method
        Returns socket object'''
        return socket.socket()
    
    def _server(self):
        '''Private method
        Used to set-up server'''
        self.soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.soc.bind(self.target)
        self.soc.listen(5)
        while True:
            self.client, self.client_addr = self.soc.accept()
            break
        return None
        
    def _client(self):
        '''Private method
        Used to connect to server'''
        try:
            self.soc.connect(self.target)
        except ConnectionRefusedError:
            print('Server refused request')
            exit()
        return None
    
    def send(self,data):
        '''Use to send data
        USAGE
        -----
        [netport object].send([data/object])
        '''
        raw_data = pickle.dumps(data)
        l = len(raw_data)
        self.client.send(str(l).encode())
        time.sleep(0.3)
        self.client.send(raw_data)
        return None
        
    
    def recv(self):
        """Use to recieve data
        USAGE
        -----
        [netport object].recv()
        """
        try:
            l = int(str(self.client.recv(1024))[2:-1])
        except ValueError:
            print("Client Disconnected!")
            exit()
        raw_data = self.client.recv(l)
        data = pickle.loads(raw_data)
        return data