'''
Created on Feb 7, 2012

@author: david
'''

from rdflib import OWL, RDF, RDFS, XSD

class StandardNS(object):
    '''
    classdocs
    '''
    __snsHandler = dict()

    def __init__(self):
        self.__snsHandler["owl"] = self.__owlNamespace()
        self.__snsHandler["rdf"] = self.__rdfNamespace()
        self.__snsHandler["rdfs"] = self.__rdfsNamespace()
        self.__snsHandler["xsd"] = self.__xsdNamespace()


    def getSnsHandler(self):
        return self.__snsHandler


    def __owlNamespace(self):
        owlHandler = dict()
        owlHandler["Class"] = OWL.Class
        owlHandler["ObjectProperty"] = OWL.ObjectProperty
        owlHandler["DatatypeProperty"] = OWL.DatatypeProperty
        owlHandler["Restriction"] = OWL.Restriction
        owlHandler["onProperty"] = OWL.onProperty
        owlHandler["maxCardinality"] = OWL.maxCardinality        
        return owlHandler
        
        
    def __rdfNamespace(self):
        rdfHandler = dict()
        rdfHandler["Property"] = RDF.Property
        rdfHandler["type"] = RDF.type
        rdfHandler["datatype"] = RDF.datatype
        return rdfHandler
        
        
    def __rdfsNamespace(self):
        rdfsHandler = dict()
        rdfsHandler["subClassOf"] = RDFS.subClassOf
        rdfsHandler["domain"] = RDFS.domain
        rdfsHandler["range"] = RDFS.range
        return rdfsHandler
        
        
    def __xsdNamespace(self):
        xsdHandler = dict()
        xsdHandler["string"] = XSD.string
        xsdHandler["int"] = XSD.int
        xsdHandler["long"] = XSD.long
        xsdHandler["float"] = XSD.float
        xsdHandler["nonNegativeInteger"] = XSD.nonNegativeInteger
        return xsdHandler