'''
Created on Mar 18, 2012

@author: david
'''

import SocketServer
import pickle
        
class QueryServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    classdocs
    """
    
    performQuery = None

    def __init__(self, addr, handler, pq):
        SocketServer.TCPServer.__init__(self, addr, handler)
        self.performQuery = pq
        

class QSHandler(SocketServer.BaseRequestHandler):
    '''
    classdocs
    '''    

    def handle(self):
        '''
        Handler
        '''
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print ("QUERY_SERVER: sending results to the client @ %s\n" % (self.client_address[0]))
        res = self.server.performQuery(self.data)
        self.request.sendall(pickle.dumps(res))
        