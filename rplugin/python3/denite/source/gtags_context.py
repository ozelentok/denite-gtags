import os
import sys

sys.path.insert(1, os.path.dirname(__file__))
from denite_gtags import TagsBase  # pylint: disable=locally-disabled, wrong-import-position


class Source(TagsBase):
    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'gtags_context'
        self.kind = 'file'

    def get_search_flags(self):
        current_line = self.vim.current.window.cursor[0]
        file_name = self.vim.current.window.buffer.name
        return [[
            '--from-here', '{}:{}'.format(current_line, file_name),
            '--result=ctags-mod'
        ]]
