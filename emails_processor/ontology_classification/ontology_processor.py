import operator
import nltk
from nltk.corpus import brown
from nltk.stem.wordnet import WordNetLemmatizer
from gensim.models import Word2Vec
from emails_processor.ontology_classification.ontology import *
from emails_processor.data_extraction.text_processor import TextProcessor

word2vec_weight = 0.0001
classification_threshold = 1

class OntologyProcessor:
    nltk.download('wordnet')
    nltk.download('brown')
    word2vec = Word2Vec(brown.sents())
    print('word2vec ready')
    _lemmatizer = WordNetLemmatizer()

    @staticmethod
    def preprocess_ontology(ontology):
        for key, obj in ontology.items():
            if type(obj) is not dict:
                continue

            if not OntologyProcessor.is_leaf(obj):
                ontology[key] = OntologyProcessor.preprocess_ontology(obj)

            ontology[key][keywords_label] = OntologyProcessor.preprocess_keywords(obj[keywords_label])

        return ontology

    @staticmethod
    def preprocess_keywords(keywords):
        lemmatized_keywords = {OntologyProcessor._lemmatizer.lemmatize(keyword) for keyword in keywords}
        return {TextProcessor.clean(keyword) for keyword in lemmatized_keywords}

    @staticmethod
    def add_to_topic(topic, seminar):
        if OntologyProcessor.is_leaf(topic):
            topic[seminars_label] |= {seminar}
        else:
            topic[others_label][seminars_label] |= {seminar}

        return topic

    @staticmethod
    def is_leaf(topic):
        if type(topic) is not dict:
            raise ValueError('Passed argument is not a topic')

        if len(topic.items()) <= 2 and topic.get(keywords_label) is not None:
            return True

        return False

    @staticmethod
    def find_best_topic(topic_name, topic, significant_tokens):
        if OntologyProcessor.is_leaf(topic):
            return topic_name, topic

        strengths = {}
        for key, obj in topic.items():
            if type(obj) is not dict:
                continue

            strengths[key] = 0
            keywords = OntologyProcessor.extract_topic_keywords(obj)
            for token, count in significant_tokens.items():
                for keyword in keywords:
                    strengths[key] += count*OntologyProcessor._calculate_similarity(token, keyword)

        best_subtopic_name, best_subtopic_strength = max(strengths.items(), key=operator.itemgetter(1))
        if best_subtopic_strength < classification_threshold:
            return topic_name, topic

        return OntologyProcessor.find_best_topic(best_subtopic_name, topic[best_subtopic_name], significant_tokens)

    @staticmethod
    def extract_topic(topic_name, ontology):
        names = ontology.keys()
        if topic_name in names:
            return ontology[topic_name]

        for _, child in ontology.items():
            if type(child) is not dict or OntologyProcessor.is_leaf(child):
                continue

            topic = OntologyProcessor.extract_topic(topic_name, child)
            if topic:
                return topic

        return None

    @staticmethod
    def extract_topic_keywords(topic):
        top_keywords = topic[keywords_label]
        children_keywords = set()
        for key, obj in topic.items():
            if type(obj) is not dict:
                continue

            children_keywords |= OntologyProcessor.extract_topic_keywords(obj)

        return top_keywords | children_keywords

    @staticmethod
    def extract_topic_seminars(topic):
        if OntologyProcessor.is_leaf(topic):
            return topic[seminars_label]

        seminars = set()
        for _, subtopic in topic.items():
            if type(subtopic) is not dict:
                continue

            seminars |= OntologyProcessor.extract_topic_seminars(subtopic)

        return seminars

    @staticmethod
    def pprint_seminars_count(ontology, indentation_count=0):
        indentation = ' ' * indentation_count
        if indentation_count > 0:
            indentation = indentation + '- '

        for key, obj in ontology.items():
            if type(obj) is not dict:
                continue

            seminars_count = len(OntologyProcessor.extract_topic_seminars(obj))
            print('{}{}({})'.format(indentation, key, str(seminars_count)))
            OntologyProcessor.pprint_seminars_count(obj, indentation_count+2)

    @staticmethod
    def _calculate_similarity(w1, w2):
        if w1 == w2:
            return 1

        try:
            similarity = OntologyProcessor.word2vec.similarity(w1, w2)
            return similarity * word2vec_weight
        except KeyError:
            return 0
