import re

import nltk
from dateutil import parser as date_parser

from emails_processor.data_extraction.text_processor import TextProcessor
from emails_processor.regular_expressions import *


class DataExtractor:
    def __init__(self, seminar_files, names_file):
        nltk.download('averaged_perceptron_tagger')

        # names_content = names_file.readlines()
        # self.names = {line.strip().lower() for line in names_content}
        # print(self.names)

        seminars = [file.read() for file in seminar_files]
        self.known_speakers = set()
        self.known_locations = set()
        for sem in seminars:
            self.known_speakers |= TextProcessor.extract_xml_tags_content(sem, 'speaker', return_as_set=True)
            self.known_locations |= TextProcessor.extract_xml_tags_content(sem, 'location', return_as_set=True)

        self.known_locations = {TextProcessor.clean(loc.lower()) for loc in self.known_locations}
        self.known_speakers = {TextProcessor.clean(spk.lower()) for spk in self.known_speakers}

    def extract_times(self, header):
        start_end_regx = re.compile(start_end_time_regx_str.format(time_regx_str))
        start_end_match = start_end_regx.search(header)
        if start_end_match:
            stime = date_parser.parse(start_end_match.group(1)).time()
            etime = date_parser.parse(start_end_match.group(2)).time()
            return stime, etime

        start_regx = re.compile(start_time_regx_str.format(time_regx_str))
        start_match = start_regx.search(header)
        if start_match:
            stime = date_parser.parse(start_match.group(1)).time()
            return stime, None

        return None, None

    def extract_locations(self, header, body):
        location_regx = re.compile(location_regx_str, re.IGNORECASE)
        locations = {match.group(1) for match in location_regx.finditer(header)}
        locations |= {match.group(1) for match in location_regx.finditer(body)}
        self.known_locations |= locations # we treat locations found in header as real locations

        pos_location_regx = re.compile(pos_location_regx_str, re.IGNORECASE)
        tagged_body = self.tag_parts_of_speech(body)
        tagged_locations = {match.group(1) for match in pos_location_regx.finditer(tagged_body)}
        tagged_locations = {re.sub(pos_tags_regx_str, '', location).strip() for location in tagged_locations}
        tagged_locations = \
            set(filter(lambda loc: TextProcessor.clean(loc.lower()) in self.known_locations, tagged_locations))
        return locations | tagged_locations

    def extract_speakers(self, header, body):
        speaker_regx = re.compile(speaker_regx_str)
        speakers = {match.group(1) for match in speaker_regx.finditer(header)}
        speakers |= {match.group(1) for match in speaker_regx.finditer(body)}
        self.known_speakers |= speakers

        tagged_body = self.tag_parts_of_speech(body)
        pos_person_regx = re.compile(pos_person_regx_str)
        tagged_people = {match.group(1) for match in pos_person_regx.finditer(tagged_body)}
        people = {re.sub(pos_tags_regx_str, '', person).strip() for person in tagged_people}
        people = set(filter(lambda person: TextProcessor.clean(person.lower()) in self.known_speakers, people))

        pos_titled_person_regx = re.compile(pos_titled_person_regx_str)
        tagged_titled_people = {match.group(1) for match in pos_titled_person_regx.finditer(tagged_body)}
        titled_people = {re.sub(pos_tags_regx_str, '', person).strip() for person in tagged_titled_people}

        # pos_person_verb_regx = re.compile(pos_person_verb_regx_str)
        # tagged_verb_people = {match.group(1) for match in pos_person_verb_regx.finditer(tagged_body)}
        # verb_people = {re.sub(pos_tags_regx_str, '', person).strip() for person in tagged_verb_people}
        # tagged_ners = self.extract_ners(tagged_body)
        # ners = {re.sub(pos_tags_regx_str, '', ner).strip() for ner in tagged_ners}
        # people = set(filter(lambda ner: any(ner_part.lower() in self.names for ner_part in ner.split(' ')), ners))
        # #print(people)
        # people = set(filter(lambda person: all(person_part.lower() not in titled_person.lower()
        #                                        for person_part in person.split(' ')
        #                                        for titled_person in titled_people), people))

        return speakers | titled_people | people # | verb_people

    # def extract_ners(self, tagged_body):
    #     pos_ner_regx = re.compile(pos_ner_regx_str)
    #     ners = {match.group(1) for match in pos_ner_regx.finditer(tagged_body)}
    #     return ners

    def tag_parts_of_speech(self, body):
        processed_body = nltk.word_tokenize(body)
        processed_body = nltk.pos_tag(processed_body)
        processed_body = ['{}{{*{}*}}'.format(word, tag) for (word, tag) in processed_body]
        return ' '.join(processed_body)


