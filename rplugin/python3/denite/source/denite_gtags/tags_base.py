import re
import os
import pathlib

from denite.source.base import Base  # pylint: disable=locally-disabled, import-error
from denite_gtags import GtagsBase  # pylint: disable=locally-disabled, wrong-import-position


class TagsBase(GtagsBase):

    TAG_PATTERN = re.compile('([^\t]+)\t(\\d+)\t(.*)')

    @classmethod
    def convert_to_candidates(cls, context, tags):
        if len(context['args']) > 0:
            word = context['args'][0]
        else:
            word = context['input']

        candidates = []
        for tag in tags:
            path, line, text = cls._parse_tag(tag)
            try:
                relpath = pathlib.Path(path).relative_to(context['path']).as_posix()
            except ValueError:
                relpath = os.path.relpath(path, context['path'])
                relpath = min([relpath, path], key=len)

            col = text.find(word) + 1
            position = f"{line}:{col:>3}"
            candidates.append({
                'word': f"{relpath:<35.35} [{position:>10}] {text}",
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
