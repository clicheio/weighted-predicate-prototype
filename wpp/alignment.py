import functools

from rdflib.graph import Graph
from rdflib.namespace import RDF
from rdflib.util import guess_format

__all__ = ('align_graphs', 'align_graphs_from_files', 'combined_probability',
           'correspondence', 'entity_pairs', 'object_equivalance')


def combined_probability(probs):
    if not probs:
        return 0.0

    product_of_probs = functools.reduce(lambda x, y: x*y, probs)
    product_of_c_probs = map(lambda x: 1.0-x, probs)
    product_of_c_probs = functools.reduce(lambda x, y: x*y,
                                          product_of_c_probs)

    return product_of_probs / (product_of_probs + product_of_c_probs)


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
        if not type_set_1:
            continue
        for entity_2 in entities_2:
            type_2 = ontology_2.value(entity_2, RDF.type)
            if type_2 not in type_set_1:
                continue
            yield (entity_1, entity_2)


def object_equivalance(object_1, object_2,
                       predicate_1, predicate_2, parameters):
    """return the similarity of the objects of the two predicates
    in two entities ranges from 0 to 1
    """

    # FIXME: currently this function consider only the case
    #        where max cardinality of a predicate is 1.
    #        a object argment should be a list of objects.

    # when objects are in the same prior matching,
    # return the confidence of the matching
    prior_correspondences = parameters['correspondences']
    cached_correspondence = prior_correspondences.get((object_1, object_2))
    if cached_correspondence:
        return cached_correspondence

    # FIXME: should compare the objects accurately according
    #        to their types and predicates
    if object_1 == object_2:
        return 1.0
    else:
        return 0.0


def correspondence(entity_1, entity_2, ontology_1, ontology_2, parameters):
    """return the confidence of that the two entities are how much similar"""

    # FIXME: currently this function consider only the case
    #        where max cardinality of a predicate is 1.
    #        later, multiple values of a predicate could be appeared.

    # make the dictionary to retrieving the set of similar predicates
    # in 'predicate_equivalances' when given a predicate
    predicate_equivalance_dict = dict()
    for pe in parameters['predicate_equivalances']:
        predicate_set = pe[0]
        for p in predicate_set:
            predicate_equivalance_dict[p] = pe

    # calculate the combined probability of the probabilities, each of which
    # is the probability of that the two entities are the same
    # when the two predicates are the same.
    # in short, the combined probability is the probability of that
    # the two entities are the same.
    stmts_1 = ontology_1.triples((entity_1, None, None))
    probs = []
    for s_1, p_1, o_1 in stmts_1:
        pe = predicate_equivalance_dict.get(p_1)
        if not pe:
            continue
        predicate_set = pe[0]
        predicate_prob = pe[1]
        stmts_2 = ontology_2.triples((entity_2, None, None))
        for s_2, p_2, o_2 in stmts_2:
            if p_2 not in predicate_set:
                continue
            probs.append(
                predicate_prob * object_equivalance(o_1, o_2, p_1, p_2,
                                                    parameters)
            )
            break
    return combined_probability(probs)


def align_graphs(ontology_1, ontology_2, parameters):
    """align ontology graphs and return the correspondences between
    the entities in the two ontologies
    """

    common_args = (ontology_1, ontology_2, parameters)

    # process ontology alignment.
    # get each pair of entities between the ontology graphs to match.
    for p in entity_pairs(*common_args):
        # get the confidence of the correspondence of the pair
        confidence = correspondence(p[0], p[1], *common_args)
        # yield correspondence
        yield (p[0], p[1], confidence)


def align_graphs_from_files(ontology_path_1, ontology_path_2,
                            param_path, format=None):
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
