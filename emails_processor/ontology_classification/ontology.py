import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from emails_processor.data_extraction.text_processor import TextProcessor

others_label = 'Others'
keywords_label = 'keywords'
seminars_label = 'seminars'

seminars_ontology = {
            'Computer Science': {
                'Software Engineering': {
                    keywords_label: {'software', 'object-oriented'},
                    seminars_label: set()
                },

                'AI': {
                    keywords_label: {'artificial', 'intelligence', 'machine learning', 'ai', 'robotics', 'vision',
                                     'nlp', 'natural language processing', 'ieee', 'navigation', 'robot', 'humanoid',
                                     'autonomous', 'knowledge', 'language', 'decision',' navigation'},
                    seminars_label: set()
                },

                'HCI': {
                    keywords_label: {'human', 'user', 'friendly', 'interaction', 'graphics', 'fun', 'usable', 'design'},
                    seminars_label: set()
                },

                'Parallel Computing': {
                    keywords_label: {'parallel', 'distributed', 'network', 'synchronization', 'efficient',
                                     'synchronous', 'asynchronous', 'thread', 'multi'},
                    seminars_label: set()
                },

                'Cyber Security': {
                    keywords_label: {'breach', 'cryptography', 'backdoor', 'encryption', 'decryption', 'hacking'},
                    seminars_label: set()
                },

                others_label: {
                    keywords_label: set(),
                    seminars_label: set()
                },

                keywords_label: {'computer', 'information', 'digital'}
            },

            others_label: {
                keywords_label: set(),
                seminars_label: set()
            },

            'TODO_DELETE': {
                keywords_label: set(),
                seminars_label: set()
            }
        }


class Ontology:
    def __init__(self, ontology=seminars_ontology):
        nltk.download('wordnet')
        self.lemmatizer = WordNetLemmatizer()
        self.ontology = self._preprocess_ontology(ontology)

    @staticmethod
    def is_leaf(topic):
        if len(topic.items()) <= 2:
            return True

        return False

    @staticmethod
    def get_topic_keywords(topic):
        top_keywords = topic[keywords_label]
        children_keywords = set()
        for key, obj in topic.items():
            if type(obj) is not dict:
                continue

            children_keywords |= Ontology.get_topic_keywords(obj)

        return top_keywords | children_keywords

    @staticmethod
    def get_topic_seminars(topic):
        return topic[seminars_label]

    @staticmethod
    def get_others(topic):
        if Ontology.is_leaf(topic):
            raise ValueError('Given topic is a leaf node so its already classified, it does not have others topic')

        return topic[others_label]

    def add_to_others(self, seminar, ontology=None):
        if not ontology:
            ontology = self.ontology

        ontology[others_label].update(seminar)
        return ontology

    def get_ontology(self):
        return self.ontology

    def get_topic(self, topic_name, ontology=None):
        if not ontology:
            ontology = self.ontology

        names = ontology.keys()
        if topic_name in names:
            return ontology[topic_name]

        for _, child in ontology.items():
            if type(child) is not dict or Ontology.is_leaf(child):
                continue

            topic = self.get_topic(topic_name, child)
            if topic:
                return topic

        return None

    def _preprocess_ontology(self, ontology):
        for key, obj in ontology.items():
            if type(obj) is not dict:
                continue

            if not Ontology.is_leaf(obj):
                ontology[key] = self._preprocess_ontology(obj)

            ontology[key][keywords_label] = self._preprocess_keywords(obj[keywords_label])

        return ontology

    def _preprocess_keywords(self, keywords):
        lemmatized_keywords = {self.lemmatizer.lemmatize(keyword) for keyword in keywords}
        return {TextProcessor.clean(keyword) for keyword in lemmatized_keywords}


