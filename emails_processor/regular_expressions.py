header_body_regx_str = r'([\s\S]+(?:\b.+\b:.+\n\n|\bAbstract\b:))([\s\S]*)'

paragraph_regx_str = r'(?<=\n\n)(?:(?:\s*\b.+\b:(?:.|\s)+?)|(\s{0,4}[A-Za-z0-9](?:.|\n)+?\s*))(?=\n\n)'
not_sentence_regx_str = r'^[A-Za-z0-9](?:.|\n)+(?:\.|\?|!|:)$'

location_regx_str = r'(?:\b(?:Place|Location|Where)\b:\s*)(.*)'
pos_location_regx_str = r'((?:(?:(?:\w*?{\*(?:NNP|CD)\*})|(?:room{\*.+?\*}))\s*)*)'

speaker_regx_str = r'(?:\b(?:Speaker|Name|Who)\b:\s*)(.*?,|.*)'
pos_person_regx_str = r'((?:\w+?{\*NNP\*}\s{0,3}){1,5})'
pos_titled_person_regx_str = r'((?:Dr|Mr|Ms|Mrs|Prof|Sir|Professor)\.?{\*NNP\*}\s{0,3}(?:\w+?{\*NNP\*}\s{0,3}){1,5})'
pos_person_verb_regx_str = r'((?:[\w\.]+?{\*NNP\*}\s{0,3}){1,5})\w+?{\*VB.?\*}'


time_regx_str = r'\b([0-9]{1,2}(?::[0-9]{2}\s?(?:AM|PM|am|pm|a\.m|p\.m)|:[0-9]{2}|\s?(?:AM|PM|am|pm|a\.m|p\.m)))\b'
start_end_time_regx_str = r'(?:\bTime\b:\s*){0}(?:\s*(?:-|until)?\s*){0}'
start_time_regx_str = r'(?:\bTime\b:\s*)({0})'

# pos_ner_regx_str = r'((?:[\w\.]+?{\*NNP\*}\s{0,3}){2,4})'
pos_tags_regx_str = r'{\*.+?\*}'
