from .gtags_def import TagsBase

class Source(TagsBase):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'gtags_file'
        self.kind = 'file'

    def on_init(self, context):
        context['__filename'] = self.vim.current.buffer.name

    def get_search_flags(self):
        return ['-f', '--result=ctags-mod']

    def get_search_word(self, context):
        return context['__filename']
