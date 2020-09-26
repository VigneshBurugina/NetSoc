import socket
import pickle
import os
import time

class netsoc:
    '''
    Wrapper for socket module for 
    easy transmission of python objects and files

    USAGE
    -----
    create an object by:
    [var]= netsoc(role of app,[target])

    ATTRIBUTES
    ----------
    self.role - Role of netsoc object [server/client]
    self.target - Address of server (default - locallost:8000)
    self.soc - socket object
    self.localhost - localhost
    self.client - client connection for server and self.soc for client

    METHODS
    -------
    Refer to method declarations for their usage

    [netsoc object].send
    [netsoc object].recv

    DEPENDENCIES - os,socket,time,pickle
    '''
    
    file_path = os.getcwd()+'/'

    def __init__(self,role,target=('localhost',8000)):
        '''Constructor for netsoc class'''
        self.role = role
        self.target = target
        self.soc = self._getsoc()
        if self.role == 'client':
            self._client()
            self.other_node = self.soc
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
            self.other_node, self.client_addr = self.soc.accept()
            break
        return None
        
    def _client(self):
        '''Private method
        Used to connect to server'''
        try:
            self.soc.connect(self.target)
        except socket.ConnectionRefusedError:
            print('Server refused request')
            exit()
        return None
    
    def send(self,data,file=False):
        '''Use to send data
        USAGE
        -----
        [netport object].send(data/object,[file=(True/False)])
        '''
        if file:
            print(file)
            with open(data,'rb') as fl:
                print(fl)
                raw_data = fl.read()
                print(raw_data)
                self.other_node.send(str(len(raw_data)).encode())
                time.sleep(0.3)
                self.other_node.send(raw_data)
                return None
        raw_data = pickle.dumps(data)
        l = len(raw_data)
        self.other_node.send(str(l).encode())
        time.sleep(0.3)
        self.other_node.send(raw_data)
        return None
        
    
    def recv(self,file=False,file_name=''):
        """Use to recieve data or files
        USAGE
        -----
        [netport object].recv([file=(True/False)],[file_name])
        """
        try:
            l = int(str(self.other_node.recv(1024))[2:-1])
        except ValueError:
            print("Client Disconnected!")
            exit()
        raw_data = self.other_node.recv(l)
        if file:
            if file_name != '':
                with open(self.file_path+file_name,'wb') as fl:
                    fl.write(raw_data)
                    print('file recved')
                    fl.close()
                print(self.file_path+file_name)
                return None
            else:
                print("Enter a valid file path")
                exit()
            return True
        data = pickle.loads(raw_data)
        return data
