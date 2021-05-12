import os
import sys

sys.path.insert(1, os.path.dirname(__file__))
from denite_gtags import TagsBase  # pylint: disable=locally-disabled, wrong-import-position


class Source(TagsBase):
    def __init__(self, vim):
        super().__init__(vim)

        self.name = "gtags_file"
        self.kind = "file"
        self.vars = {"options": ["-f", "--result=ctags-mod"]}

    def on_init(self, context):
        context["__filename"] = self.vim.current.buffer.name

    def get_search_flags(self):
        return [self.vars["options"]]

    def _get_search_word(self, context):
        return context["__filename"]

    @classmethod
    def convert_to_candidates(cls, context, tags):
        candidates = []

        for tag in tags:
            path, word, line, *text = tag.split(" ")
            text = " ".join(text)
            col = text.find(word) + 1
            candidate = {
                "word": word,
                "action__path": path,
                "action__line": line,
                "action__col": col,
                "action__text": text,
            }
            candidates.append(candidate)
            position = f"{line}:{col:>3}"
            candidate["abbr"] = f"{word:<50.50} [{position:>10}] {text}"

        return candidates
