from emails_processor.ontology_classification.ontology import seminars_ontology
from emails_processor.ontology_classification.ontology_classifier import OntologyClassifier

root = '../../data/test_untagged/'
files_range = range(301, 485)
files = [open('{}{}.txt'.format(root, i), 'r') for i in files_range]

classifier = OntologyClassifier(seminars_ontology)
for f in files:
    classifier.add(f)

print('\nClassified seminars count per topic:')
classifier.pprint(2)