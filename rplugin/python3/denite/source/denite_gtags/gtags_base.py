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

    def _exec_global(self, search_args, context):
        command = ['global', '-q'] + search_args
        global_proc = subprocess.Popen(command,
                                       cwd=context['path'],
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
            self._print_global_error(global_exitcode, err_output)
            return []

        return [t for t in output.split('\n') if len(t) > 0]

    def _print_global_error(self, global_exitcode, err_output):
        if global_exitcode == 1:
            error_message = '[denite-gtags] Error: file does not exists'
        elif global_exitcode == 2:
            error_message = '[denite-gtags] Error: invalid arguments\n{}'.format(err_output)
        elif global_exitcode == 3:
            error_message = '[denite-gtags] Error: GTAGS not found'
        elif global_exitcode == 126:
            error_message = '[denite-gtags] Error: permission denied\n{}'.format(err_output)
        elif global_exitcode == 127:
            error_message = '[denite-gtags] Error: \'global\' command not found\n{}'
        else:
            error_message = '[denite-gtags] Error: global command failed\n{}'.format(err_output)
        denite.util.error(self.vim, error_message)


class Source(Base):
    pass
