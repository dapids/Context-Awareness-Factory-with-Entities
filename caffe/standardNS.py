'''
Created on Feb 7, 2012

@author: david
'''

from rdflib import OWL, RDF, RDFS, XSD

class StandardNS(object):
    '''
    Provides a dictionary of dictionaries containing all the needed tags for OWL, RDF, RDFS, XSD.
    '''
    __snsHandler = dict()

    def __init__(self):
        '''
        Creates a dictionary of dictionaries containing all the needed tags for OWL, RDF, RDFS, XSD.
        '''
        self.__snsHandler["owl"] = self.__owlNamespace()
        self.__snsHandler["rdf"] = self.__rdfNamespace()
        self.__snsHandler["rdfs"] = self.__rdfsNamespace()
        self.__snsHandler["xsd"] = self.__xsdNamespace()


    def getSnsHandler(self):
        '''
        @return: a dictionary of dictionaries containing all the needed tags for OWL, RDF, RDFS, XSD
        '''
        return self.__snsHandler


    def __owlNamespace(self):
        '''
        @return: a dictionary containing all the needed tags for OWL
        '''
        owlHandler = dict()
        owlHandler["Class"] = OWL.Class
        owlHandler["ObjectProperty"] = OWL.ObjectProperty
        owlHandler["DatatypeProperty"] = OWL.DatatypeProperty
        owlHandler["Restriction"] = OWL.Restriction
        owlHandler["onProperty"] = OWL.onProperty
        owlHandler["maxCardinality"] = OWL.maxCardinality        
        return owlHandler
        
        
    def __rdfNamespace(self):
        '''
        @return: a dictionary containing all the needed tags for RDF
        '''
        rdfHandler = dict()
        rdfHandler["Property"] = RDF.Property
        rdfHandler["type"] = RDF.type
        rdfHandler["datatype"] = RDF.datatype
        return rdfHandler
        
        
    def __rdfsNamespace(self):
        '''
        @return: a dictionary containing all the needed tags for RDFS
        '''
        rdfsHandler = dict()
        rdfsHandler["subClassOf"] = RDFS.subClassOf
        rdfsHandler["domain"] = RDFS.domain
        rdfsHandler["range"] = RDFS.range
        return rdfsHandler
        
        
    def __xsdNamespace(self):
        '''
        @return: a dictionary containing all the needed tags for XSD
        '''
        xsdHandler = dict()
        xsdHandler["string"] = XSD.string
        xsdHandler["int"] = XSD.int
        xsdHandler["long"] = XSD.long
        xsdHandler["float"] = XSD.float
        xsdHandler["nonNegativeInteger"] = XSD.nonNegativeInteger
        return xsdHandler