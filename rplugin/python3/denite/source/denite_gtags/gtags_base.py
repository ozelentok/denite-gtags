import os
import subprocess
from abc import abstractmethod
from denite.source.base import Base  # pylint: disable=locally-disabled, import-error
import denite.util  # pylint: disable=locally-disabled, import-error


class GtagsBase(Base):
    def highlight(self):
        self.vim.command(f"highlight default link {self.syntax_name}_Position Comment")

    def define_syntax(self):
        self.vim.command(
            f"syntax match {self.syntax_name}_Position /"
            r" \[.\{-}\]"
            f"/ contained containedin={self.syntax_name}"
        )

    def gather_candidates(self, context):
        word = self._get_search_word(context)

        candidates = []
        for search_flags in self.get_search_flags():
            if word:
                search_flags += ['--', word]

            tags = self._exec_global(search_flags, context)
            candidates += self.convert_to_candidates(context, tags)

        self.print_message(context, candidates)

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

        gtags_lib_path = self.vim.vars.get("denite_gtags_lib", None)
        if isinstance(gtags_lib_path, list):
            gtags_lib_path = ":".join(gtags_lib_path)

        env = {}
        if gtags_root:
            env["GTAGSROOT"] = gtags_root
        if gtags_db_path:
            env["GTAGSDBPATH"] = gtags_db_path
        if gtags_lib_path:
            env["GTAGSLIBPATH"] = gtags_lib_path
        return env

    def _exec_global(self, search_args, context, input=None):
        command = ["global", "-a", "-q"] + search_args
        gtags_env = self._create_global_env()
        self.print_message(context, context["path"])
        self.print_message(context, " ".join(command))
        self.print_message(context, str(gtags_env))

        env = os.environ.copy()
        env.update(gtags_env)

        try:
            global_proc = subprocess.run(
                command,
                cwd=context["path"],
                universal_newlines=True,
                stdin=input,
                env=env,
                encoding="utf8",
                check=False,
                capture_output=True,
                timeout=15,
            )
        except Exception as e:
            self.error_message(context, e)
            return []

        if global_proc.returncode != 0:
            self._print_global_error(context, global_proc)
            return []

        return [t for t in global_proc.stdout.split("\n") if len(t) > 0]

    def _print_global_error(self, context, proc):
        if proc.returncode == 1:
            message = "File does not exists"
        elif proc.returncode == 2:
            message = "Invalid arguments"
        elif proc.returncode == 3:
            message = "GTAGS not found"
        elif proc.returncode == 126:
            message = "Permission denied"
        elif proc.returncode == 127:
            message = "'global' command not found"
        else:
            message = "global command failed"

        self.error_message(context, f"[Error {proc.returncode}] {message}: {proc.stderr}")
