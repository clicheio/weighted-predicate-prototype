import os

from rdflib.graph import Graph
from rdflib.term import URIRef
from rdflib.util import guess_format

from wpp.alignment import (align_graphs_from_files, combined_probability,
                           entity_pairs, voted_confidence)

ontology_path_1 = os.path.join('tests', 'ontology1.nt')
ontology_path_2 = os.path.join('tests', 'ontology2.nt')
param_path = os.path.join('tests', 'parameters.py')


# FIXME: the all test depend on the same test case.
#        (changing a test case demands also fix all the test.)
#        separate them.

def get_example():
    ontology_1 = Graph()
    ontology_1.parse(ontology_path_1, format=guess_format(ontology_path_1))

    ontology_2 = Graph()
    ontology_2.parse(ontology_path_2, format=guess_format(ontology_path_2))

    parameters = dict()
    exec(compile(open(param_path, "rb").read(), param_path, 'exec'),
         parameters)

    return ontology_1, ontology_2, parameters


def test_entity_pairs():
    ontology_1, ontology_2, parameters = get_example()
    pair_generator = entity_pairs(ontology_1, ontology_2, parameters)
    pairs = {p for p in pair_generator}
    assert pairs == {
        (URIRef('http://dbpedia.org/resource/'
                'The_Lord_of_the_Rings_(film_series)'),
         URIRef('http://cliche.io/resource/Film/The_Lord_of_the_Rings')),
        (URIRef('http://dbpedia.org/resource/Peter_Jackson'),
         URIRef('http://cliche.io/resource/Peter_Jackson')),
    }


def test_voted_confidence():
    init_conf = 0.5  # initial confidence of some fact
    user_weight = 0.1  # weight of an user vote

    conf = init_conf
    conf = voted_confidence(0.0, conf, user_weight)  # a downvote
    conf = voted_confidence(0.0, conf, user_weight)  # a downvote
    conf = voted_confidence(1.0, conf, user_weight)  # an upvote

    assert conf == 0.9*(0.9*(0.9*init_conf)) + 0.1*1.0


def test_object_equivalance():
    # FIXME: the 'object_equivalance' function is also tested in
    #        'test_align_graphs_from_files'.
    #        seperate the test case and fill this test.
    pass


def test_correspondence():
    # FIXME: the 'correspondence' function is also tested in
    #        'test_align_graphs_from_files'.
    #        seperate the test case and fill this test.
    pass


def test_align_graphs_from_files():
    res_generator = align_graphs_from_files(ontology_path_1, ontology_path_2,
                                            param_path)
    res = {c for c in res_generator}

    assert res == {
        (URIRef('http://dbpedia.org/resource/'
                'The_Lord_of_the_Rings_(film_series)'),
         URIRef('http://cliche.io/resource/Film/The_Lord_of_the_Rings'),
         combined_probability([0.1*0.9, 0.9*1.0])),
        (URIRef('http://dbpedia.org/resource/Peter_Jackson'),
         URIRef('http://cliche.io/resource/Peter_Jackson'),
         combined_probability([0.9*1.0, 0.95*1.0])),
    }


def test_combined_probability():
    probs_1 = [0.6, 0.72]
    assert combined_probability(probs_1) == \
        0.6*0.72 / (0.6*0.72 + (1-0.6)*(1-0.72))

    probs_2 = [0.1, 0.2, 0.3]
    assert combined_probability(probs_2) == \
        0.1*0.2*0.3 / (0.1*0.2*0.3 + (1-0.1)*(1-0.2)*(1-0.3))
