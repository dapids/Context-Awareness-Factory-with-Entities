'''
Created on Mar 18, 2012

@author: david
'''

import SocketServer
from threading import Thread
from .retriever import Retriever

class QueryServer(Thread):
    '''
    classdocs
    '''
    __address = None
    __globalContext = None

    def __init__(self, address, gc):
        Thread.__init__(self)
        self.__address = address
        self.__globalContext = gc
    
    
    def run(self):
        # Create the server, binding to localhost on port 9999
        server = QServer(self.__address, QHandler, self.__globalContext)
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
        
        
class QServer(SocketServer.ThreadingTCPServer):
    retriever = None
    
    def __init__(self, addr, handler, gc):
        SocketServer.ThreadingTCPServer.__init__(self, addr, handler)
        self.retriever = Retriever(gc)

class QHandler(SocketServer.BaseRequestHandler):
    '''
    classdocs
    '''    
    
    def handle(self):
        '''
        Handler
        '''
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print "{} wrote:".format(self.client_address[0])
        print self.data
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())
        