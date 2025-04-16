from src.utils import grep_files_by_extension
from src.printer import *
import subprocess


class FlutterHook:
    """helper for dart flutter"""

    def __init__(self, files: list[str]):
        self.config_file_name = 'license_checker.yaml'
        self.files = grep_files_by_extension(files, 'dart')
        self.pubspec_file_or_config_changed = 'pubspec.lock' in files or self.config_file_name in files

    def license_check(self) -> bool:
        if not self.pubspec_file_or_config_changed:
            return True
        installation_args = ["dart", "pub", "global", "activate", "license_checker"]
        subprocess.run(installation_args)
        scanning_results = ["lic_ck", "check-licenses", "--config"]
        scanning_results.append(self.config_file_name)
        license_scan_result = subprocess.run(installation_args)
        if license_scan_result.returncode != 0:
            return False
        return True

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
