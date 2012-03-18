'''
Created on Feb 24, 2012

@author: david
'''

from rdflib import ConjunctiveGraph, OWL, Literal
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
        """
        Creates a global graph representing a global context.
        @type gns: str
        @param gns: the global namespace
        """
        globalGraph = ConjunctiveGraph()
        globalGraph.bind("owl", OWL)
        globalGraph.bind(gns[gns.rfind("/")+1:len(gns)-1], gns)
        return globalGraph
        
    
    @classmethod
    def mapClass(cls, cl, gCntx, pd, rc):
        """
        Maps a class to the semantic network by means of the method __addClass.
        Also maps its super-classes by means of the method __addSuperClass.
        @type cl: type
        @param cl: the class to map
        @type gCntx: tuple
        @param gCntx: the global context in which the class should be map
        @type pd: dict
        @param pd: list of properties to pass to every class
        @type rc: Set
        @param rc: list of classes already mapped on the semantic network
        @return: the list of classes already mapped on the semantic network, after updating it
        """
        graph = gCntx[0]
        ns = gCntx[1]
        cls.__addClass(cl.__name__, graph, ns)
        rc.add(cl)
        cl.getPropsDict(pd)
        for superCl in cl.__bases__:
            if Utils.isSubOfEntity(superCl):
                cls.__addsuperClass(cl.__name__, superCl.__name__, graph, ns)
                rc.update(cls.mapClass(superCl, gCntx, pd, rc))
        return rc


    @classmethod
    def mapClassProperty(cls, name, domain, rng, cntx):
        """
        Maps a class property on the semantic networks by means of the methods
        __addObjectProperty and addDataProperty.
        Before mapping the property, it checks whether it is correct or not,
        and it gets the type of the property (object or data).
        @type name: str
        @param name: name of the property to map
        @type domain: str
        @param domain: domain of the property to map
        @type rng: object
        @param rng: range of the property to map
        @type cntx: tuple
        @param cntx: a graph and a namespace representing a global context
        """
        name = name.lower()
        graph, ns = cntx.getInfo()[1], cntx.getInfo()[2]
        try:
            typology = Utils.checkClassRange(name, domain.__name__, rng)
        except SemanticException as e:
            raise e
        else:
            if typology == "objectProperty":
                cls.__addObjectProperty(name, domain.__name__, rng.__name__, graph, ns)
            else:
                cls.__addDataProperty(name, domain.__name__, rng, graph, ns)


    @classmethod
    def mapIndividual(cls, identifier, cl, gc):
        """
        Maps an individual on the semantic network.
        @type identifier: str
        @param identifier: identifier of the individual to map
        @type cl: str
        @param cl: class which the individual belongs to
        @type gc: tuple
        @param gc: a graph and a namespace representing a global context
        """
        graph = gc.getInfo()[0]
        ns = gc.getInfo()[1]
        graph.add((ns[identifier], cls.__sns["rdf"]["type"], ns[cl]))


    @classmethod
    def mapIndProperty(cls, name, domain, rng, cntx, chars):
        """
        Maps an individual property to the semantic network by means of the methods __addIndObjproperty and
        __addIndDataProperty.
        Before doing it, it checks whether the property is an ObjectProperty or a DataProperty.
        @type name: str
        @param name: name of the property to map
        @type domain: str
        @param domain: domain of the property to map
        @type rng: str
        @param rng: range of the property to map
        @type cntx: tuple
        @param cntx: the graph and the namespace of a local context
        @type chars: str
        @param ns: characteristics of the property
        """
        name = name.lower()
        graph, ns = cntx.getInfo()[1], cntx.getInfo()[2]
        if not isinstance(rng, (int, str, float, bool)):
            cls.__addIndObjProperty(name, domain, rng.getId(), graph, ns, chars)
        else:
            cls.__addIndDataProperty(name, domain, rng, graph, ns)


    @classmethod
    def removeIndProperty(cls, name, domain, rng, cntx):
        """
        Removes an individual property to the semantic network by means of the methods __remIndObjProperty
        and __remIndDataProperty.
        Before doing it, it checks whether the property is an ObjectProperty or a DataProperty.
        @type name: str
        @param name: name of the property to remove
        @type domain: str
        @param domain: domain of the property to remove
        @type rng: str
        @param rng: range of the property to remove
        @type graph: Graph
        @param graph: local graph which the property is related to
        @type ns: Namespace
        @param ns: global namespace which the property is related to
        """
        name = name.lower()
        graph, ns = cntx.getInfo()[1], cntx.getInfo()[2]
        if not isinstance(rng, (int, str, float, bool)):
            cls.__remIndObjProperty(name, domain, rng.getId(), graph, ns)
        else:
            cls.__remIndDataProperty(name, domain, rng, graph, ns)


    @classmethod
    def __remIndObjProperty(cls, name, domain, rng, graph, ns):
        """
        Removes an individual ObjectProperty from the semantic network.
        @type name: str
        @param name: name of the property to remove
        @type domain: str
        @param domain: domain of the property to remove
        @type rng: str
        @param rng: range of the property to remove
        @type graph: Graph
        @param graph: local graph which the property is related to
        @type ns: Namespace
        @param ns: global namespace which the property is related to
        """
        graph.remove((ns[domain], ns[name], ns[rng]))


    @classmethod
    def __remIndDataProperty(cls, name, domain, rng, graph, ns):
        """
        Removes an individual DataProperty from the semantic network.
        @type name: str
        @param name: name of the property to remove
        @type domain: str
        @param domain: domain of the property to remove
        @type rng: object
        @param rng: range of the property to remove
        @type graph: Graph
        @param graph: local graph which the property is related to
        @type ns: Namespace
        @param ns: global namespace which the property is related to
        """
        if isinstance(rng, int):
            obj = Literal(rng, datatype=cls.__sns["xsd"]["int"])
        elif isinstance(rng, bool):
            obj = Literal(rng, datatype=cls.__sns["xsd"]["boolean"])
        elif isinstance(rng, float):
            obj = Literal(rng, datatype=cls.__sns["xsd"]["float"])
        else:
            obj = Literal(rng, datatype=cls.__sns["xsd"]["string"])
        graph.remove((ns[domain], ns[name], obj))
    

    @classmethod
    def __addIndObjProperty(cls, name, domain, rng, graph, ns, chars):
        """
        Adds an individual ObjectProperty to the semantic network.
        @type name: str
        @param name: name of the property to add
        @type domain: str
        @param domain: domain of the property to add
        @type rng: str
        @param rng: range of the property to add
        @type graph: Graph
        @param graph: local graph which the property is related to
        @type ns: Namespace
        @param ns: global namespace which the property is related to
        @type chars: str
        @param ns: characteristics of the property
        """
        graph.add((ns[domain], ns[name], ns[rng]))
        if chars == "s":
            graph.add((ns[rng], ns[name], ns[domain]))
    
    
    @classmethod
    def __addIndDataProperty(cls, name, domain, rng, graph, ns):
        """
        Adds an individual DataProperty to the semantic network.
        @type name: str
        @param name: name of the property to add
        @type domain: str
        @param domain: domain of the property to add
        @type rng: object
        @param rng: range of the property to add
        @type graph: Graph
        @param graph: local graph which the property is related to
        @type ns: Namespace
        @param ns: global namespace which the property is related to
        """
        if isinstance(rng, bool):
            obj = Literal(rng, datatype=cls.__sns["xsd"]["boolean"])
        elif isinstance(rng, int):
            obj = Literal(rng, datatype=cls.__sns["xsd"]["int"])
        elif isinstance(rng, float):
            obj = Literal(rng, datatype=cls.__sns["xsd"]["float"])
        else:
            obj = Literal(rng, datatype=cls.__sns["xsd"]["string"])
        graph.add((ns[domain], ns[name], obj))
    

    @classmethod
    def __addObjectProperty(cls, name, domain, rng, graph, ns):
        """
        Adds a class ObjectProperty to the semantic network.
        @type name: str
        @param name: name of the property to add
        @type domain: str
        @param domain: domain of the property to add
        @type rng: str
        @param rng: range of the property to add
        @type graph: Graph
        @param graph: local graph which the property is related to
        @type ns: Namespace
        @param ns: global namespace which the property is related to
        """
        triples = ((ns[name], cls.__sns["rdf"]["type"], cls.__sns["owl"]["ObjectProperty"]),
                    (ns[name], cls.__sns["rdfs"]["domain"], ns[domain]),
                    (ns[name], cls.__sns["rdfs"]["range"], ns[rng]))
#        a = BNode()
#        triples += ((a, cls.__sns["rdf"]["type"], cls.__sns["owl"]["Restriction"]),
#        (BNode(domain), cls.__sns["rdfs"]["subClassOf"], a),
#        (a, cls.__sns["owl"]["onProperty"], ns[name]),
#        (a, cls.__sns["owl"]["maxCardinality"], Literal("1", datatype=cls.__sns["xsd"]["nonNegativeInteger"])))
        for triple in triples:
            graph.add(triple)
            
    
    @classmethod
    def __addDataProperty(cls, name, domain, rng, graph, ns):
        """
        Adds a class DataProperty to the semantic network.
        @type name: str
        @param name: name of the property to add
        @type domain: str
        @param domain: domain of the property to add
        @type rng: type
        @param rng: range of the property to add
        @type graph: Graph
        @param graph: local graph which the property is related to
        @type ns: Namespace
        @param ns: global namespace which the property is related to
        """
        if rng is int:
            data = cls.__sns["xsd"]["int"]
        elif rng is bool:
            data = cls.__sns["xsd"]["boolean"]
        elif rng is float:
            data = cls.__sns["xsd"]["float"]
        else:
            data = cls.__sns["xsd"]["string"]
            
        triples = ((ns[name], cls.__sns["rdf"]["type"], cls.__sns["owl"]["DatatypeProperty"]),
                    (ns[name], cls.__sns["rdfs"]["domain"], ns[domain]),
                    (ns[name], cls.__sns["rdfs"]["range"], data))
#        a = BNode()
#        triples += ((a, cls.__sns["rdf"]["type"], cls.__sns["owl"]["Restriction"]),
#        (BNode(dmn), cls.__sns["rdfs"]["subClassOf"], a),
#        (a, cls.__sns["owl"]["onProperty"], ns[name]),
#        (a, cls.__sns["owl"]["maxCardinality"], Literal("1", datatype=cls.__sns["xsd"]["nonNegativeInteger"])))
        for triple in triples:
            graph.add(triple)


    @classmethod
    def __addClass(cls, name, graph, ns):
        """
        Adds a class to the semantic network.
        @type name: str
        @param name: name of the class to be mapped
        @type graph: Graph
        @param graph: graph of the context in which the class should be mapped
        @type ns: Namespace
        @param ns: namespace which the class belongs to
        """
        graph.add((ns[name], cls.__sns["rdf"]["type"], cls.__sns["owl"]["Class"]))
    

    @classmethod    
    def __addsuperClass(cls, name, superClName, graph, ns):
        """
        Adds a super-class to a class in the semantic network.
        @type name: str
        @param name: name of the class which the super-class should be related to
        @type superClName: str
        @param superClName: name of the super-class to be mapped
        @type graph: Graph
        @param graph: graph which the super-class should be mapped in
        @type ns: Namespace
        @param ns: namespace which the super-class belongs to
        """
        graph.add((ns[name], cls.__sns["rdfs"]["subClassOf"], ns[superClName]))