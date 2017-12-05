import re

from dateutil import parser as time_parser
from nltk.tokenize import sent_tokenize

from emails_processor.data_extraction.data_extractor import DataExtractor
from emails_processor.data_extraction.xml_processor import XMLProcessor
from emails_processor.regular_expressions import *


class SeminarsTagger:
    def __init__(self, seminar_files, names_file):
        self.data_extractor = DataExtractor(seminar_files, names_file)

    def tag_seminar(self, seminar_file):
        seminar = seminar_file.read().strip('\n -*')
        # separate heading from body
        header, body = re.search(header_body_regx_str, seminar).groups()
        # print(self.data_extraction.tag_parts_of_speech(body))
        header = header.rstrip('\n')
        # extracting data
        stime, etime = self.data_extractor.extract_times(header)
        locations = self.data_extractor.extract_locations(header, body)
        speakers = self.data_extractor.extract_speakers(header, body)

        # tagging
        body = self.tag_paragraphs(body)
        body = self.tag_sentences(body)

        seminar = header + '\n\n' + body
        seminar = self.tag_times(seminar, stime, etime)
        seminar = self.tag_locations(seminar, locations)
        seminar = self.tag_speakers(seminar, speakers)

        return seminar

    def tag_paragraphs(self, text):
        text = '\n\n{}\n\n'.format(text.strip('\n'))
        paragraph_regx = re.compile(paragraph_regx_str)
        for match in paragraph_regx.finditer(text):
            paragraph = match.group(1)
            if paragraph:
                text = text.replace(paragraph, '<paragraph>{}</paragraph>'.format(paragraph))

        return text.strip()

    def tag_sentences(self, text):
        text_parts = XMLProcessor.split_on_tags(text, 'paragraph')
        sentences = []
        for part in text_parts:
            sentences.extend(sent_tokenize(part.strip()))

        # filter everything that is not a proper sentence
        sentences = list(filter(lambda s: re.match(not_sentence_regx_str, s), sentences))
        for sent in sentences:
            text = text.replace(sent, '<sentence>{}</sentence>'.format(sent))

        return text

    def tag_times(self, text, stime, etime):
        if not etime and not stime:
            return text

        time_regx = re.compile(time_regx_str)
        for time_str in set(time_regx.findall(text)):
            time = time_parser.parse(time_str).time()
            if stime == time:
                text = text.replace(time_str, '<stime>{}</stime>'.format(time_str))
            elif etime == time:
                text = text.replace(time_str, '<etime>{}</etime>'.format(time_str))

        return text

    def tag_locations(self, text, locations):
        for loc in locations:
            insensitive_loc = re.compile(r'({})'.format(re.escape(loc)), re.IGNORECASE)
            text = re.sub(insensitive_loc, r'<location>\1</location>', text)

        return text

    def tag_speakers(self, text, speakers):
        for spk in speakers:
            insensitive_spk = re.compile(r'({})'.format(re.escape(spk)), re.IGNORECASE)
            # print(insensitive_loc)
            text = re.sub(insensitive_spk, r'<speaker>\1</speaker>', text)

        return text
