import os
import sys

sys.path.insert(1, os.path.dirname(__file__))
from denite_gtags import GtagsBase # pylint: disable=locally-disabled, wrong-import-position

class Source(GtagsBase):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'gtags_path'
        self.kind = 'file'

    @classmethod
    def get_search_flags(cls):
        return ['-P']

    @classmethod
    def convert_to_candidates(cls, tags):
        return [{'word': t, 'action__path': t} for t in tags]
