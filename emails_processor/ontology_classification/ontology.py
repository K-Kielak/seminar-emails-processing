import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from emails_processor.data_extraction.text_processor import TextProcessor

keywords_label = 'keywords'
seminars_label = 'seminars'
others_label = 'Others'

seminars_ontology = {
            'Computer Science': {
                'Software Engineering': {
                    keywords_label: {'software', 'object-oriented'},
                    seminars_label: {}
                },

                'AI': {
                    keywords_label: {'artificial', 'intelligence', 'machine learning', 'ai', 'robotics', 'vision',
                                     'nlp', 'natural language processing', 'ieee', 'navigation', 'robot', 'humanoid',
                                     'autonomous', 'knowledge', 'language', 'decision',' navigation'},
                    seminars_label: {}
                },

                'HCI': {
                    keywords_label: {'human', 'user', 'friendly', 'interaction', 'graphics', 'fun', 'usable', 'design'},
                    seminars_label: {}
                },

                'Parallel Computing': {
                    keywords_label: {'parallel', 'distributed', 'network', 'synchronization', 'efficient',
                                     'synchronous', 'asynchronous', 'thread', 'multi'},
                    seminars_label: {}
                },

                'Cyber Security': {
                    keywords_label: {'breach', 'cryptography', 'backdoor', 'encryption', 'decryption', 'hacking'},
                    seminars_label: {}
                },

                others_label: {
                    keywords_label: {},
                    seminars_label: {}
                },

                keywords_label: {'computer', 'information', 'digital'}
            },

            others_label: {
                keywords_label: {}
            }
        }


class Ontology:
    def __init__(self, ontology=seminars_ontology):
        nltk.download('wordnet')
        self.lemmatizer = WordNetLemmatizer()
        self.ontology = self._preprocess_ontology(ontology)

    @staticmethod
    def get_topic_keywords(topic):
        top_keywords = topic[keywords_label]
        children_keywords = set()
        for key, obj in topic.items():
            if type(obj) is list:
                continue

            children_keywords |= Ontology.get_topic_keywords(obj)

        return top_keywords | children_keywords

    @staticmethod
    def get_topic_seminars(topic):
        return topic[seminars_label]

    def add_to_others(self, seminar, ontology=None):
        if not ontology:
            ontology = self.ontology

        ontology[others_label].update(seminar)
        return ontology

    def get_ontology(self):
        return self.ontology

    def get_topic(self, key, ontology=None):
        if type(ontology) is list:
            return None

        if not ontology:
            ontology = self.ontology

        keys = ontology.keys()
        if key in keys:
            return ontology[key]

        for child in keys:
            topic = self.get_topic(key, ontology[child])
            if topic:
                return topic

        return None

    def _preprocess_ontology(self, ontology):
        for key, obj in ontology.items():
            if type(obj) is list:
                continue

            ontology[key] = self._preprocess_ontology(obj)
            ontology[key][keywords_label] = self._preprocess_keywords(obj[keywords_label])

        return ontology

    def _preprocess_keywords(self, keywords):
        lemmatized_keywords = {self.lemmatizer.lemmatize(keyword) for keyword in keywords}
        return {TextProcessor.clean(keyword) for keyword in lemmatized_keywords}




