import subprocess
from denite.source.base import Base # pylint: disable=locally-disabled, import-error
import denite.util # pylint: disable=locally-disabled, import-error

class GtagsBase(Base):

    def exec_global(self, search_args, context):
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
            self.print_global_error(global_exitcode, err_output)
            return []

        return [t for t in output.split('\n') if len(t) > 0]

    def print_global_error(self, global_exitcode, err_output):
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
