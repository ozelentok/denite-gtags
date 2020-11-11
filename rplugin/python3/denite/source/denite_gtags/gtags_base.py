import os
import subprocess
from abc import abstractmethod
from denite.source.base import Base  # pylint: disable=locally-disabled, import-error
import denite.util  # pylint: disable=locally-disabled, import-error


class GtagsBase(Base):
    def gather_candidates(self, context):
        word = self._get_search_word(context)

        candidates = []
        for search_flags in self.get_search_flags():
            if word:
                search_flags += ['--', word]

            tags = self._exec_global(search_flags, context)
            candidates += self.convert_to_candidates(tags)

        return candidates

    @abstractmethod
    def get_search_flags(self):
        return [[]]

    @abstractmethod
    def convert_to_candidates(self):
        raise NotImplementedError()

    def _get_search_word(self, context):
        args_count = len(context['args'])
        if args_count > 0:
            return context['args'][0]

        return context['input']

    def _create_global_env(self):
        buffer_vars = self.vim.current.buffer.vars
        gtags_root = buffer_vars.get('denite_gtags_root', None)
        gtags_db_path = buffer_vars.get('denite_gtags_db_path', None)
        global_env = os.environ.copy()
        if gtags_root:
            global_env['GTAGSROOT'] = gtags_root
        if gtags_db_path:
            global_env['GTAGSDBPATH'] = gtags_db_path
        return global_env

    def _exec_global(self, search_args, context, input=None):
        command = ['global', '-q'] + search_args
        global_proc = subprocess.Popen(
            command,
            cwd=context['path'],
            universal_newlines=True,
            stdin=subprocess.PIPE if input else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=self._create_global_env())
        try:
            output, error = global_proc.communicate(input=input, timeout=15)
        except subprocess.TimeoutExpired:
            global_proc.kill()
            output, error = global_proc.communicate()
        global_exitcode = global_proc.returncode

        if global_exitcode != 0:
            self._print_global_error(global_exitcode, error)
            return []

        return [t for t in output.split('\n') if len(t) > 0]

    def _print_global_error(self, global_exitcode, error):
        if global_exitcode == 1:
            message = '[denite-gtags] Error: File does not exists'
        elif global_exitcode == 2:
            message = '[denite-gtags] Error: Invalid arguments\n{error}'
        elif global_exitcode == 3:
            message = '[denite-gtags] Error: GTAGS not found'
        elif global_exitcode == 126:
            message = f'[denite-gtags] Error: Permission denied\n{error}'
        elif global_exitcode == 127:
            message = '[denite-gtags] Error: \'global\' command not found'
        else:
            message = '[denite-gtags] Error: global command failed\n{error}'
        denite.util.error(self.vim, message)
