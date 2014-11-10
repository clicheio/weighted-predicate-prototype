from setuptools import setup

packages = {
    'wpp',
}

install_requires = {
    'rdflib >= 4.1.2',
}

tests_require = {
    'pytest >= 2.5.0',
}

setup(
    name='weighted-predicate-prototype',
    version='0.0',
    description='ontology matching prototype with weighted predicate',
    url='https://github.com/clicheio/weighted-predicate-prototype',
    author='The Cliche team',
    packages=packages,
    install_requires=install_requires,
    extras_require={
        'tests': tests_require,
    },
)
