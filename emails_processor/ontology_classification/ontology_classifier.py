import re
import nltk
from collections import Counter
from nltk.stem.wordnet import WordNetLemmatizer
from emails_processor.data_extraction.text_processor import TextProcessor
from emails_processor.ontology_classification.ontology_processor import OntologyProcessor

from emails_processor.regular_expressions import *


class OntologyClassifier:
    def __init__(self, ontology):
        nltk.download('wordnet')
        self.lemmatizer = WordNetLemmatizer()
        self.ontology = OntologyProcessor.preprocess_ontology(ontology)

    # adds seminar to one of the internal ontology's topics and returns name of the topic
    def add(self, seminar_file):
        seminar = seminar_file.read().strip('\n -*')
        topic_name, topic = self.classify(seminar)
        OntologyProcessor.add_to_topic(topic, seminar)
        if OntologyProcessor.is_leaf(topic):
            return topic_name

        # if doesn't match any specific category, add to others
        return str(topic_name) + ' - Others'

    def classify(self, seminar):
        # separate heading from body
        header, body = re.search(header_body_regx_str, seminar).groups()
        header = header.rstrip('\n')

        # classification
        topic_name, topic = self._analyze_header(header)
        topic_name, topic = self._analyze_body(body, topic_name, topic)
        if OntologyProcessor.is_leaf(topic):
            return topic_name, topic

        return topic_name, topic

    # Try to classify seminar based on its header, return None if unsuccessful
    def _analyze_header(self, header):
        type_regx = re.compile(type_regx_str, re.IGNORECASE)
        significant_lines = [match.group(1) for match in type_regx.finditer(header)]
        significant_tokens = set()
        for line in significant_lines:
            significant_tokens |= set(re.split(r'[.,\s]', line))

        significant_tokens = [self.lemmatizer.lemmatize(token).lower() for token in significant_tokens]
        significant_tokens = [TextProcessor.clean(token).lower() for token in significant_tokens]
        significant_tokens = Counter(significant_tokens)
        return OntologyProcessor.find_best_topic('Top', self.ontology, significant_tokens)

    # doesn't do anything at the moment TODO implement
    def _analyze_body(self, body, topic_name, topic):
        return topic_name, topic

