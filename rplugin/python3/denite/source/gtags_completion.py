import os
import sys

sys.path.insert(1, os.path.dirname(__file__))
from denite_gtags import GtagsBase # pylint: disable=locally-disabled, wrong-import-position

class Source(GtagsBase):
    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'gtags_completion'
        self.kind = GtagsCompletionKind(vim)

    @classmethod
    def get_search_flags(cls):
        return ['-c']

    def gather_candidates(self, context):
        tags = self.exec_global(self.get_search_flags(), context)
        candidates = self._convert_to_candidates(tags)
        return candidates

    @classmethod
    def _convert_to_candidates(cls, tags):
        return [{'word': t} for t in tags]


class GtagsCompletionKind(object):
    def __init__(self, vim):
        self.vim = vim
        self.name = 'gtags_completion_kind'
        self.default_action = 'list_all'
        self.redraw_actions = ['list_defs', 'list_refs', 'list_all']
        self.persist_actions = []

    def action_list_defs(self, context):
        self._action(context, 'gtags_def:{}')

    def action_list_refs(self, context):
        self._action(context, 'gtags_ref:{}')

    def action_list_all(self, context):
        self._action(context, 'gtags_def:{0} gtags_ref:{0}')

    def _action(self, context, sources_format):
        denite_cmd_prefix = 'Denite -mode=normal '

        for target in context['targets']:
            sources = sources_format.format(target['word'])
            self.vim.command(denite_cmd_prefix + sources)

