import os
import sys

sys.path.insert(1, os.path.dirname(__file__))
from denite_gtags import TagsBase  # pylint: disable=locally-disabled, wrong-import-position


class Source(TagsBase):
    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'gtags_files'
        self.kind = 'file'

    def on_init(self, context):
        context['__dir_path'] = context['path']
        if self.vim.current.buffer.name:
            context['__dir_path'] = os.path.dirname(
                self.vim.current.buffer.name)

    def get_search_flags(self):
        return [['-f', '--result=ctags-mod', '-L', '-']]

    def gather_candidates(self, context):
        dir_path = context['__dir_path']
        file_paths = '\n'.join(
            self._exec_global(['-P', '-S', dir_path], context))

        candidates = []
        for search_flags in self.get_search_flags():
            tags = self._exec_global(search_flags, context, file_paths)
            candidates += self.convert_to_candidates(tags)

        return candidates
