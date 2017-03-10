import subprocess
import re
from abc import abstractmethod
import denite.util

from .base import Base

class GtagsBase(Base):

    def exec_global(self, search_args):
        command = ['global', '-q'] + search_args
        global_proc = subprocess.Popen(command,
                                       universal_newlines=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
        try:
            output, err_output = global_proc.communicate(timeout=15)
        except subprocess.TimeoutExpired:
            global_proc.kill()
            output, err_output = global_proc.communicate()
        global_exitcode = global_proc.returncode

        if global_exitcode != 0:
            self.print_global_error(global_exitcode, err_output)
            return []

        return [t for t in output.split('\n') if len(t) > 0]

    def print_global_error(self, global_exitcode, err_output):
        if global_exitcode == 1:
            error_message = '[denite-gtags] Error: file does not exists'
        elif global_exitcode == 2:
            error_message = '[denite-gtags] Error: invalid argumnets\n{}'.format(err_output)
        elif global_exitcode == 3:
            error_message = '[denite-gtags] Error: GTAGS not found'
        elif global_exitcode == 126:
            error_message = '[denite-gtags] Error: permission denied\n{}'.format(err_output)
        elif global_exitcode == 127:
            error_message = '[denite-gtags] Error: \'global\' command not found\n{}'
        else:
            error_message = '[denite-gtags] Error: global command failed\n{}'.format(err_output)
        denite.util.error(self.vim, error_message)

class TagsBase(GtagsBase):

    TAG_PATTERN = re.compile('(.*)\t(\\d+)\t(.*)')

    def __init__(self, vim):
        super().__init__(vim)

    @abstractmethod
    def get_search_flags(self):
        return []

    def get_search_word(self, context):
        if len(context['args']) > 0:
            return context['args'][0]
        return context['input']

    def gather_candidates(self, context):
        word = self.get_search_word(context)
        tags = self.exec_global(self.get_search_flags() + [word])
        candidates = self._convert_to_candidates(tags)
        return candidates

    @classmethod
    def _convert_to_candidates(cls, tags):
        candidates = []
        for tag in tags:
            path, line, text = cls._parse_tag(tag)
            col = text.find(text) -1
            candidates.append({
                'word': tag,
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

class Source(TagsBase):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'gtags_def'
        self.kind = 'file'

    def get_search_flags(self):
        return ['-d', '--result=ctags-mod']
