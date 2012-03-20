'''
Created on Mar 18, 2012

@author: david
'''

from rdflib import plugin, query
import pyparsing

class Retriever(object):
    '''
    classdocs
    '''

    __globalContext = None


    def __init__(self, gc):
        '''
        Constructor
        '''
        self.__globalContext = gc
        plugin.register("sparql", query.Processor, "rdfextras.sparql.processor", "Processor")
        plugin.register("sparql", query.Result, "rdfextras.sparql.query", "SPARQLQueryResult")
        
    
    def performQuery(self, request):
        result = list()
        try:
            q = self.__globalContext[0].query(request,
                                              initNs = {self.__globalContext[2]: self.__globalContext[1]})
        except StandardError as e:
            print e
        except pyparsing.ParseException as e:
            print e
        else:
            result = q.result
        return result