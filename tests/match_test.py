import os

from rdflib.graph import Graph
from rdflib.term import URIRef
from rdflib.util import guess_format

from wpp.alignment import align_graphs_from_files, entity_pairs

ontology_path_1 = os.path.join('tests', 'ontology1.nt')
ontology_path_2 = os.path.join('tests', 'ontology2.nt')
param_path = os.path.join('tests', 'parameters.py')


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


def test_correspondence():
    # FIXME: fill this test after the 'correspondence' function is completed
    pass


def test_align_graphs_from_files():
    res_generator = align_graphs_from_files(ontology_path_1, ontology_path_2,
                                            param_path)

    # FIXME: fix the RHS of the assert statment for the result checking
    # after complete the 'correspondence' function
    res = {c for c in res_generator}
    assert res == {
        (URIRef('http://dbpedia.org/resource/'
                'The_Lord_of_the_Rings_(film_series)'),
         URIRef('http://cliche.io/resource/Film/The_Lord_of_the_Rings'),
         1.0),
        (URIRef('http://dbpedia.org/resource/Peter_Jackson'),
         URIRef('http://cliche.io/resource/Peter_Jackson'),
         1.0),
    }
