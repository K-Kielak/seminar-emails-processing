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
            }
        }
