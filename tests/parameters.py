from rdflib.term import URIRef

# the correspondences between the two entities with confidence measure
correspondences = [
    (
        URIRef('http://dbpedia.org/resource/'
               'The_Lord_of_the_Rings_(film_series)'),
        URIRef('http://cliche.io/resource/film/The_Lord_of_the_Rings'),
        0.9,
    ),
    (
        URIRef('http://dbpedia.org/resource/'
               'The_Lord_of_the_Rings_(film_series)'),
        URIRef('http://cliche.io/resource/film/Cardcaptor_Sakura'),
        0.5,
    ),
]

# the similar predicates and the probability of that the entities of
# the two predicates are the same when the objects of the two predicates
# are the same
# FIXME: the probability should be evaluated by data distribution
property_equivalance = [
    (
        {
            URIRef('http://dbpedia.org/ontology/birthDate'),
            URIRef('http://cliche.io/ontology/birthDate'),
        },
        0.95
    ),
    (
        {
            URIRef('http://xmlns.com/foaf/0.1/name'),
            URIRef('http://xmlns.com/foaf/0.1/name'),
        },
        0.9
    ),
]

# the sets of the types of which the entities are to be matched each other
types_to_be_matched = [
    {
        URIRef('http://dbpedia.org/ontology/Film'),
        URIRef('http://dbtropes.org/resource/Main/Film'),
        URIRef('http://cliche.io/ontology/Film'),
    },
    {
        URIRef('http://dbpedia.org/ontology/Agent'),
        URIRef('http://cliche.io/ontology/Person'),
    },
]
