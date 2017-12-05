from emails_processor.tagging.seminars_tagger import SeminarsTagger

# given
tagged_files_range = range(0, 301)
tagged_files_root = '../../data/training/'
names_file_root = '../../data/names/'
untagged_files_root = '../../data/test_untagged/'

file_number_to_tag = 481  # <INSERT NUMBER OF FILE TO TAG (301-485) HERE IF YOU WANT TO CHANGE IT>

# when
training_files = [open('{}{}.txt'.format(tagged_files_root, i), 'r') for i in tagged_files_range]
names_file = open('{}names.txt'.format(names_file_root), 'r')
tagger = SeminarsTagger(training_files, names_file)
seminar_file = open('{}{}.txt'.format(untagged_files_root, file_number_to_tag))
output_file = open('text.txt', 'w')

# then
output_file.write(tagger.tag_seminar(seminar_file))
