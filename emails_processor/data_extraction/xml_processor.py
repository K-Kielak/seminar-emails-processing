import re


class XMLProcessor:
    @staticmethod
    def split_on_tags(text, tag):
        return re.split(r'</?{}>'.format(tag), text)

    @staticmethod
    def extract_tags_content(text, tag, return_clean=False, return_as_set=False):
        regex = re.compile(r'<{0}>[ \t]*((?:.|\s)+?)[ \t]*</{0}>'.format(tag), re.M)
        tags_content = regex.findall(text)
        if return_clean and return_as_set:
            return {XMLProcessor.clean(content) for content in tags_content}

        if return_clean:
            return [XMLProcessor.clean(content) for content in tags_content]

        if return_as_set:
            return {content for content in tags_content}

        return tags_content

    @staticmethod
    def clean(text):
        # clean tags
        text = re.sub(r"<.+?>", "", text)

        # clean text from non-alphanumeric characters so eg. <sentence>sentence</sentence> is the same as
        # <sentence>sentence.</sentence> because such details doesn't really matter for future information
        # extraction etc.
        return re.sub(r'\W', '', text)
