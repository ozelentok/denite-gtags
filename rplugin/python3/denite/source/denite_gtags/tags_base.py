import re
from abc import abstractmethod
from denite_gtags import GtagsBase # pylint: disable=locally-disabled, wrong-import-position

class TagsBase(GtagsBase):

    TAG_PATTERN = re.compile('(.*)\t(\\d+)\t(.*)')

    def __init__(self, vim):
        super().__init__(vim)

    @abstractmethod
    def get_search_flags(self):
        return []

    def get_search_word(self, context):
        if len(context['args']) > 0:
            return context['args'][0]
        return context['input']

    def gather_candidates(self, context):
        word = self.get_search_word(context)
        tags = self.exec_global(self.get_search_flags() + [word], context)
        candidates = self._convert_to_candidates(tags)
        return candidates

    @classmethod
    def _convert_to_candidates(cls, tags):
        candidates = []
        for tag in tags:
            path, line, text = cls._parse_tag(tag)
            col = text.find(text) -1
            candidates.append({
                'word': tag,
                'action__path': path,
                'action__line': line,
                'action__text': text,
                'action__col': col
            })
        return candidates

    @classmethod
    def _parse_tag(cls, tag):
        match = cls.TAG_PATTERN.match(tag)
        return match.groups()
