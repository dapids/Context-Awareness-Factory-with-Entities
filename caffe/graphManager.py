'''
Created on Feb 24, 2012

@author: david
'''

from rdflib import ConjunctiveGraph, OWL, BNode, Literal
from .standardNS import StandardNS
from .tools.exceptions import SemanticException
from .tools.utils import Utils

class GraphManager(object):
    '''
    classdocs
    '''
    
    
    __sns = StandardNS().getSnsHandler()

    
    @classmethod
    def createGlobalGraph(cls, gns):
        globalGraph = ConjunctiveGraph()
        globalGraph.bind("owl", OWL)
        globalGraph.bind(gns[gns.rfind("/")+1:len(gns)-1], gns)
        return globalGraph
        
    
    @classmethod
    def mapClass(cls, cl, gCntx, pd, rc):
        graph = gCntx[0]
        ns = gCntx[1]
        cls.__addClass(cl.__name__, graph)
        rc.add(cl)
        cl.getPropsDict(pd)
        for superCl in cl.__bases__:
            if Utils.isSubOfEntity(superCl):
                cls.__addsuperClass(cl.__name__, superCl.__name__, graph, ns)
                rc.update(cls.mapClass(superCl, gCntx, pd, rc))
        return rc


    @classmethod
    def mapClassProperty(cls, name, domain, rng, cntx):
        name = name.lower()
        graph, ns = cntx.getInfo()[1], cntx.getInfo()[2]
        try:
            typology = Utils.checkClassRange(name, domain, rng)
        except SemanticException as e:
            raise e
        else:
            if typology == "objectProperty":
                cls.__addObjectProperty(name, domain.__name__, rng.__name__, graph, ns)
            else:
                cls.__addDataProperty(name, domain.__name__, rng, graph, ns)


    @classmethod
    def mapIndividual(cls, name, cl, gc):
        graph = gc.getInfo()[0]
        ns = gc.getInfo()[1]
        graph.add((BNode(name), cls.__sns["rdf"]["type"], ns[cl]))


    @classmethod
    def mapIndProperty(cls, name, domain, rng, cntx):
        name = name.lower()
        graph, ns = cntx.getInfo()[1], cntx.getInfo()[2]
        if not isinstance(rng, (int, str, float, long)):
            cls.__addIndObjProperty(name, domain.getName(), rng.getName(), graph, ns)
        else:
            cls.__addIndDataProperty(name, domain.getName(), rng, graph, ns)


    @classmethod
    def removeIndProperty(cls, name, domain, rng, cntx):
        name = name.lower()
        graph, ns = cntx.getInfo()[1], cntx.getInfo()[2]
        if not isinstance(rng, (int, str, float, long)):
            cls.__remIndObjProperty(name, domain, rng.getName(), graph, ns)
        else:
            cls.__remIndDataProperty(name, domain, rng, graph, ns)


    @classmethod
    def __remIndObjProperty(cls, name, domain, rng, graph, ns):
        graph.remove((BNode(domain), ns[name], ns[rng]))


    @classmethod
    def __remIndDataProperty(cls, name, domain, rng, graph, ns):
        if isinstance(rng, int):
            obj = Literal(rng, datatype=cls.__sns["xsd"]["int"])
        elif isinstance(rng, long):
            obj = Literal(rng, datatype=cls.__sns["xsd"]["long"])
        elif isinstance(rng, float):
            obj = Literal(rng, datatype=cls.__sns["xsd"]["float"])
        else:
            obj = Literal(rng, datatype=cls.__sns["xsd"]["string"])
        graph.remove((BNode(domain), ns[name], obj))
    

    @classmethod
    def __addIndObjProperty(cls, name, domain, rng, graph, ns):
        graph.add((BNode(domain), ns[name], ns[rng]))
    
    
    @classmethod
    def __addIndDataProperty(cls, name, domain, rng, graph, ns):
        if isinstance(rng, int):
            obj = Literal(rng, datatype=cls.__sns["xsd"]["int"])
        elif isinstance(rng, long):
            obj = Literal(rng, datatype=cls.__sns["xsd"]["long"])
        elif isinstance(rng, float):
            obj = Literal(rng, datatype=cls.__sns["xsd"]["float"])
        else:
            obj = Literal(rng, datatype=cls.__sns["xsd"]["string"])
        graph.add((BNode(domain), ns[name], obj))
    

    @classmethod
    def __addObjectProperty(cls, name, domain, rng, graph, ns):
        triples = ((BNode(name), cls.__sns["rdf"]["type"], cls.__sns["owl"]["ObjectProperty"]),
                    (BNode(name), cls.__sns["rdfs"]["domain"], ns[domain]),
                    (BNode(name), cls.__sns["rdfs"]["range"], ns[rng]))
#        a = BNode()
#        triples += ((a, cls.__sns["rdf"]["type"], cls.__sns["owl"]["Restriction"]),
#        (BNode(domain), cls.__sns["rdfs"]["subClassOf"], a),
#        (a, cls.__sns["owl"]["onProperty"], ns[name]),
#        (a, cls.__sns["owl"]["maxCardinality"], Literal("1", datatype=cls.__sns["xsd"]["nonNegativeInteger"])))
        for triple in triples:
            graph.add(triple)
            
    
    @classmethod
    def __addDataProperty(cls, name, domain, rng, graph, ns):
        if rng is int:
            datatype = Literal(None, datatype=cls.__sns["xsd"]["int"])
        elif rng is long:
            datatype = Literal(None, datatype=cls.__sns["xsd"]["long"])
        elif rng is float:
            datatype = Literal(None, datatype=cls.__sns["xsd"]["float"])
        else:
            datatype = Literal(None, datatype=cls.__sns["xsd"]["string"])
            
        triples = ((BNode(name), cls.__sns["rdf"]["type"], cls.__sns["owl"]["DatatypeProperty"]),
                    (BNode(name), cls.__sns["rdfs"]["domain"], ns[domain]),
                    (BNode(name), cls.__sns["rdfs"]["range"], datatype))
#        a = BNode()
#        triples += ((a, cls.__sns["rdf"]["type"], cls.__sns["owl"]["Restriction"]),
#        (BNode(dmn), cls.__sns["rdfs"]["subClassOf"], a),
#        (a, cls.__sns["owl"]["onProperty"], ns[name]),
#        (a, cls.__sns["owl"]["maxCardinality"], Literal("1", datatype=cls.__sns["xsd"]["nonNegativeInteger"])))
        for triple in triples:
            graph.add(triple)


    @classmethod
    def __addClass(cls, name, graph):
        graph.add((BNode(name), cls.__sns["rdf"]["type"], cls.__sns["owl"]["Class"]))
    

    @classmethod    
    def __addsuperClass(cls, name, superClName, graph, ns):
        graph.add((BNode(name), cls.__sns["rdfs"]["subClassOf"], ns[superClName]))