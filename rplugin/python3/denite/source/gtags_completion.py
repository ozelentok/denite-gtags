import os
import sys

sys.path.insert(1, os.path.dirname(__file__))
from denite_gtags import GtagsBase # pylint: disable=locally-disabled, wrong-import-position

class Source(GtagsBase):

    _ACTION_COMMAND_TEMPLATE = 'Denite -mode=normal gtags_def:{0} gtags_ref:{0}'

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'gtags_completion'
        self.kind = 'command'

    @classmethod
    def get_search_flags(cls):
        return ['-c']

    def gather_candidates(self, context):
        tags = self.exec_global(self.get_search_flags(), context)
        candidates = self._convert_to_candidates(tags)
        return candidates

    @classmethod
    def _convert_to_candidates(cls, tags):
        return [{'word': t, 'action__command': cls._ACTION_COMMAND_TEMPLATE.format(t)} for t in tags]
