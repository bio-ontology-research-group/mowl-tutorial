import mowl
mowl.init_jvm('2g')

import os
from java.util import HashSet
from mowl.owlapi import OWLAPIAdapter
from org.semanticweb.owlapi.model import IRI

def main():
    adapter = OWLAPIAdapter()
    ontology = adapter.create_ontology("http://mowl/family")
    male = adapter.create_class("http://Male")
    female = adapter.create_class("http://Female")
    parent = adapter.create_class("http://Parent")
    person = adapter.create_class("http://Person")
    mother = adapter.create_class("http://Mother")
    father = adapter.create_class("http://Father")
    has_child = adapter.create_object_property("http://hasChild")
    John = adapter.create_individual("http://John")
    Jane = adapter.create_individual("http://Jane")
    Robert = adapter.create_individual("http://Robert")
    Melissa = adapter.create_individual("http://Melissa")

    axioms = HashSet()
    axioms.add(adapter.create_subclass_of(male, person))
    axioms.add(adapter.create_subclass_of(female, person))
    axioms.add(adapter.create_subclass_of(parent, person))
    axioms.add(adapter.create_subclass_of(mother, female))
    axioms.add(adapter.create_subclass_of(father, male))
    axioms.add(adapter.create_disjoint_classes(male, female))
    parent_and_male = adapter.create_object_intersection_of(parent, male)
    axioms.add(adapter.create_subclass_of(parent_and_male, father))
    parent_and_female = adapter.create_object_intersection_of(parent, female)
    axioms.add(adapter.create_subclass_of(parent_and_female, mother))
    male_or_female = adapter.create_object_union_of(male, female)
    axioms.add(adapter.create_equivalent_classes(male_or_female, person))
    not_male = adapter.create_complement_of(male)
    axioms.add(adapter.create_equivalent_classes(not_male, female))
    has_child_person = adapter.create_object_some_values_from(
        has_child, person)
    axioms.add(adapter.create_subclass_of(parent, has_child_person))
    axioms.add(adapter.create_class_assertion(father, John))
    axioms.add(adapter.create_class_assertion(mother, Jane))
    axioms.add(adapter.create_class_assertion(male, Robert))
    axioms.add(adapter.create_class_assertion(female, Melissa))
    axioms.add(adapter.create_object_property_assertion(has_child, John, Robert))
    axioms.add(adapter.create_object_property_assertion(has_child, Jane, Robert))
    axioms.add(adapter.create_object_property_assertion(has_child, John, Melissa))
    axioms.add(adapter.create_object_property_assertion(has_child, Jane, Melissa))
    adapter.owl_manager.addAxioms(ontology, axioms)
    ont_file = os.path.abspath(f'family.owl')
    adapter.owl_manager.saveOntology(ontology, IRI.create('file://' + ont_file))
        


if __name__ == '__main__':
    main()
