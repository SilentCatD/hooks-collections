from src.git_ignore_parser import parse_gitignore
from src.printer import *
import os


def grep_files_by_extension(files: list[str], extension: str) -> list[str]:
    """filter files by the extension"""
    results = []
    for file in files:
        file_names = file.split('.')
        if len(file_names) < 2:
            continue
        file_extension = file_names[-1]
        if file_extension == extension:
            results.append(file)
    return results


def filter_by_hooks_ignore(file_names: list[str]) -> list[str]:
    """filter files by ignore pattern found in `.hooksignore`"""
    hooks_ignore_file = '.hooksignore'
    if os.path.exists(hooks_ignore_file):
        ignorer = parse_gitignore(hooks_ignore_file)
    else:
        info("no .hooksignore specified")
        return file_names

    result = []
    for file_name in file_names:
        ignore = ignorer(file_name)
        if not ignore:
            result.append(file_name)
    return result


def filter_by_existence(file_names: list[str]) -> list[str]:
    """filter only available files on disk"""
    result = []
    for file_name in file_names:
        if os.path.exists(file_name):
            result.append(file_name)
    return result


def is_in_ci():
    """check is in ci env"""
    return os.getenv("GITHUB_ACTIONS") == "true" or os.getenv("TRAVIS") == "true" or os.getenv(
        "CIRCLECI") == "true" or os.getenv("GITLAB_CI") == "true"
