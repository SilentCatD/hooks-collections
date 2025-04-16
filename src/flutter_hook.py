from src.utils import grep_files_by_extension
from src.printer import *
import subprocess


class FlutterHook:
    """helper for dart flutter"""
    def __init__(self, files: list[str]):
        self.files = grep_files_by_extension(files, 'dart')

    def format_files(self) -> bool:
        """format dart files"""
        if not self.files:
            ok("No changes made to Dart file, skip formatting!")
            return True
        info("Formatting...")
        args_list = ["dart", "format"]
        args_list.extend(self.files)
        run_result = subprocess.run(args_list)
        if run_result.returncode != 0:
            return False
        return True

    def lint_files(self) -> bool:
        """linting dart files"""
        if not self.files:
            ok("No changes made to Dart file, skip lint!")
            return True
        info("Linting...")
        args_list = ["dart", "analyze", "--fatal-infos", "--fatal-warnings"]
        args_list.extend(self.files)
        run_result = subprocess.run(args_list)
        if run_result.returncode != 0:
            return False
        return True

    def fix_files(self) -> bool:
        """apply lint fix to files one by one"""
        if not self.files:
            ok("No changes made to Dart file, skip fixing!")
            return True
        info("Applying fix...")
        args_list = ["dart", "fix", "--apply"]
        for file in self.files:
            args_list.append(file)
            run_result = subprocess.run(args_list)
            if run_result.returncode != 0:
                return False
            args_list.pop()
        return True
