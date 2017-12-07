from tabulate import tabulate
from emails_processor.data_extraction.text_processor import TextProcessor
from emails_processor.tagging.seminars_tagger import SeminarsTagger


def evaluate(tagsets, test_tagsets):
    print('********************************************')
    true_positivies = 0 # exists in both tagset and test_tagset
    false_positives = 0 # exists in tagset but does not exist in test_tagset
    false_negatives = 0 # does not exist in tagset but exists in test_tagset
    for i in range(0, len(tagsets)):
        set = tagsets[i]
        test_set = test_tagsets[i]
        for tag in set:
            if tag in test_set:
                true_positivies += 1
            else:
                false_positives += 1
                print(tag + ' (wrong, seminar {})'.format(i))

        for test_tag in test_set:
            if test_tag not in set:
                false_negatives += 1
                print(test_tag + ' (not catched, seminar {})'.format(i))

    # print(true_positivies)
    # print(false_negatives)
    # print(false_positives)
    precision = true_positivies / (true_positivies + false_positives)
    recall = true_positivies / (true_positivies + false_negatives)
    f_measure = 0
    if precision + recall > 0:
        f_measure = (precision * recall) / (precision + recall)

    return precision, recall, f_measure

# given
training_files_range = range(0, 301)
training_files_root = '../../data/training/'
test_files_range = range(301, 485)
untagged_files_root = '../../data/test_untagged/'
tagged_test_files_root = '../../data/test_tagged/'

# when
tagged_test_seminars = [open('{}{}.txt'.format(tagged_test_files_root, i), 'r').read() for i in test_files_range]

# get tags content for test data
test_paragraphs = [TextProcessor.extract_xml_tags_content(tagged_seminar, 'paragraph',
                                                          return_clean=True, return_as_set=True)
                   for tagged_seminar in tagged_test_seminars]

test_sentences = [TextProcessor.extract_xml_tags_content(tagged_seminar, 'sentence',
                                                         return_clean=True, return_as_set=True)
                  for tagged_seminar in tagged_test_seminars]

test_stimes = [TextProcessor.extract_xml_tags_content(tagged_seminar, 'stime', return_as_set=True)
               for tagged_seminar in tagged_test_seminars]

test_etimes = [TextProcessor.extract_xml_tags_content(tagged_seminar, 'etime', return_as_set=True)
               for tagged_seminar in tagged_test_seminars]

test_locations = [TextProcessor.extract_xml_tags_content(tagged_seminar, 'location', return_clean=True, return_as_set=True)
                  for tagged_seminar in tagged_test_seminars]

test_speakers = [TextProcessor.extract_xml_tags_content(tagged_seminar, 'speaker', return_clean=True, return_as_set=True)
                 for tagged_seminar in tagged_test_seminars]


# get tags content for the program
training_files = [open('{}{}.txt'.format(training_files_root, i), 'r') for i in training_files_range]
untagged_files = [open('{}{}.txt'.format(untagged_files_root, i), 'r') for i in test_files_range]

tagger = SeminarsTagger(training_files)
tagged_seminars = [tagger.tag_seminar(seminar) for seminar in untagged_files]

paragraphs = [TextProcessor.extract_xml_tags_content(tagged_seminar, 'paragraph',
                                                     return_clean=True, return_as_set=True)
              for tagged_seminar in tagged_seminars]

sentences = [TextProcessor.extract_xml_tags_content(tagged_seminar, 'sentence',
                                                    return_clean=True, return_as_set=True)
             for tagged_seminar in tagged_seminars]

stimes = [TextProcessor.extract_xml_tags_content(tagged_seminar, 'stime', return_as_set=True)
          for tagged_seminar in tagged_seminars]

etimes = [TextProcessor.extract_xml_tags_content(tagged_seminar, 'etime', return_as_set=True)
          for tagged_seminar in tagged_seminars]

locations = [TextProcessor.extract_xml_tags_content(tagged_seminar, 'location', return_clean=True, return_as_set=True)
             for tagged_seminar in tagged_seminars]

speakers = [TextProcessor.extract_xml_tags_content(tagged_seminar, 'speaker', return_clean=True, return_as_set=True)
            for tagged_seminar in tagged_seminars]

# then
paragraph_stats = evaluate(paragraphs, test_paragraphs)
sentence_stats = evaluate(sentences, test_sentences)
etime_stats = evaluate(etimes, test_etimes)
stime_stats = evaluate(stimes, test_stimes)
location_stats = evaluate(locations, test_locations)
speakers_stats = evaluate(speakers, test_speakers)
# spk_precision, spk_recall, spk_f_measure = evaluate(speakers, test_speakers)
print(tabulate([('paragraph',) + paragraph_stats,
                ('sentence',) + sentence_stats,
                ('etime',) + etime_stats,
                ('stime',) + stime_stats,
                ('location',) + location_stats,
                ('speaker',) + speakers_stats],
               headers=['Tag', 'Precision', 'Recall', 'F Measure']))






