from rdflib.graph import Graph
from rdflib.namespace import RDF
from rdflib.util import guess_format

__all__ = ('align_graphs', 'align_graphs_from_files', 'correspondence',
           'entity_pairs')


def entity_pairs(ontology_1, ontology_2, parameters):
    """get all the pairs of entities between the ontology graphs to match"""

    types_to_be_matched = parameters['types_to_be_matched']

    # make the dictionary to retrieving the set in 'types_to_be_matched'
    # when given a type
    type_sets = dict()
    for s in types_to_be_matched:
        for t in s:
            type_sets[t] = s

    # get all the entities in the ontologies
    entities_1 = set()
    entities_2 = set()
    for s, p, o in ontology_1:
        entities_1.add(s)
    for s, p, o in ontology_2:
        entities_2.add(s)

    # get all the pairs to yield
    for entity_1 in entities_1:
        type_1 = ontology_1.value(entity_1, RDF.type)
        type_set_1 = type_sets.get(type_1)
        if not type_set_1: continue
        for entity_2 in entities_2:
            type_2 = ontology_2.value(entity_2, RDF.type)
            if not type_2 in type_set_1: continue
            yield (entity_1, entity_2)


def correspondence(entity_1, entity_2, ontology_1, ontology_2, parameters):
    """return the confidence of that the two entities are how much similar"""

    # FIXME: fill this function
    return 1.0

def align_graphs(ontology_1, ontology_2, parameters):
    """align ontology graphs and return the correspondences between
    the entities in the two ontologies
    """

    common_args = (ontology_1, ontology_2, parameters)

    # process ontology alignment
    # get each pair of entities between the ontology graphs to match
    for p in entity_pairs(*common_args):
        # get the confidence of the correspondence of the pair
        confidence = correspondence(p[0], p[1], *common_args)
        # yield correspondence
        yield (p[0], p[1], confidence)


def align_graphs_from_files(ontology_path_1,
                            ontology_path_2,
                            param_path,
                            format=None):
    """align ontology graphs from RDF files in 'ontology_path_1'
    and 'ontology_path_2' with the help of parameters
    from the file in 'param_path'
    """

    # get graphs from files
    if not format:
        ontology_1 = Graph()
        ontology_1.parse(ontology_path_1,
                         format=guess_format(ontology_path_1))
        ontology_2 = Graph()
        ontology_2.parse(ontology_path_2,
                         format=guess_format(ontology_path_2))
    else:
        ontology_1 = Graph(ontology_path_1, format=format)
        ontology_2 = Graph(ontology_path_2, format=format)

    # get parameters for alignment from file
    parameters = dict()
    exec(compile(open(param_path, "rb").read(), param_path, 'exec'),
         parameters)

    # align graphs with parameters
    yield from align_graphs(ontology_1, ontology_2, parameters)
