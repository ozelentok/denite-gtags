from .gtags_def import TagsBase

class Source(TagsBase):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'gtags_grep'
        self.kind = 'file'

    def get_search_flags(self):
        return ['-g', '--result=ctags-mod']
