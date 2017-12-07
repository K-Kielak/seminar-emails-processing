import re
import nltk
import operator
from collections import Counter
from nltk.stem.wordnet import WordNetLemmatizer
from emails_processor.data_extraction.text_processor import TextProcessor
from emails_processor.ontology_classification.ontology import Ontology

from emails_processor.regular_expressions import *


class OntologyClassifier:
    def __init__(self):
        nltk.download('wordnet')
        self.lemmatizer = WordNetLemmatizer()
        self.ontology = Ontology()

    def classify(self, seminar_file):
        seminar = seminar_file.read().strip('\n -*')

        # separate heading from body
        header, body = re.search(header_body_regx_str, seminar).groups()
        header = header.rstrip('\n')

        # classification
        topic_name, topic = self.analyze_header(header)
        topic_name, topic = self.analyze_body(body, topic_name, topic)
        if Ontology.is_leaf(topic):
            return topic_name

        return Ontology.get_others(topic)

    # Try to classify seminar based on its header, return None if unsuccessful
    def analyze_header(self, header):
        type_regx = re.compile(type_regx_str, re.IGNORECASE)
        significant_lines = [match.group(1) for match in type_regx.finditer(header)]
        significant_tokens = set()
        for line in significant_lines:
            significant_tokens |= set(re.split(r'[.,\s]', line))

        significant_tokens = [self.lemmatizer.lemmatize(token).lower() for token in significant_tokens]
        significant_tokens = [TextProcessor.clean(token).lower() for token in significant_tokens]
        significant_tokens = Counter(significant_tokens)
        return self.find_best_topic('Top', self.ontology.get_ontology(), significant_tokens)

    # doesn't do anything at the moment TODO implement
    def analyze_body(self, body, topic_name, topic):
        return topic_name, topic

    def find_best_topic(self, topic_name, topic, significant_tokens):
        if Ontology.is_leaf(topic):
            return topic_name, topic

        strengths = {}
        for key, obj in topic.items():
            if type(obj) is not dict:
                continue

            strengths[key] = 0
            keywords = Ontology.get_topic_keywords(obj)
            for token, count in significant_tokens.items():
                if token in keywords:
                    strengths[key] += count

        print(strengths)
        best_subtopic_name, best_subtopic_strength = max(strengths.items(), key=operator.itemgetter(1))
        if best_subtopic_strength is 0:
            return topic_name, topic

        return self.find_best_topic(best_subtopic_name, topic[best_subtopic_name], significant_tokens)
