import os
import sys

sys.path.insert(1, os.path.dirname(__file__))
from denite_gtags import TagsBase  # pylint: disable=locally-disabled, wrong-import-position


class Source(TagsBase):
    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'gtags_ref'
        self.kind = 'file'

    def highlight(self):
        super().highlight()
        self.vim.command(f"highlight default link {self.syntax_name}_Word Function")

    def define_syntax(self):
        super().define_syntax()

        word = self._get_search_word(self.context)
        self.vim.command(f"syntax match {self.syntax_name}_Word /"
                         f"\\<{word}\\>"
                         f"/ contained containedin={self.syntax_name}")

    def get_search_flags(self):
        return [['-rs', '--result=ctags-mod']]
