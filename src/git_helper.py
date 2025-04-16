from subprocess import CalledProcessError

from src.printer import *
from src.utils import filter_by_hooks_ignore, filter_by_existence
import subprocess
import sys


def set_commit_template(path):
    subprocess.check_call(['git', 'config', 'commit.template', path])


def unset_commit_template():
    subprocess.check_call(['git', 'config', '--unset', 'commit.template'])


def get_git_root_dir():
    """get repository root path"""
    output = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], encoding='utf-8').strip()
    return str(output)


def get_commit_msg_file():
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        file_name = '.git/COMMIT_EDITMSG'
        warn("get commit message run outside of intended scope: commit-msg, prepare-commit-msg")
    return file_name


def get_commit_msg(file: str = None):
    """get next commit message either passed from the system or the default one"""
    file_name = file if file is not None else get_commit_msg_file()
    with open(file_name) as f:
        commit_message = f.read()
    return commit_message


def get_git_diff(staged: bool = True):
    args = ['git', 'diff']
    if staged:
        args.append('--staged')
    return subprocess.check_output(args, encoding='utf-8').strip()


def get_not_resolved_files(staged: bool = True):
    """get files that still have unresolved conflicts"""
    args = ["git", "diff", "--check", "-w"]
    if staged:
        args.append("--staged")
    try:
        output = subprocess.check_output(args, encoding='utf-8').strip()
        if output:
            err(output)
            return output.split('\n')
        return []
    except CalledProcessError as e:
        newline = '\n'
        newline_tab = '\n\t'
        problems = str(e.output).strip().split(newline)
        err(f"Conflicts content detected:{newline_tab}{newline_tab.join(problems)}")
        return problems


def all_conflict_resolved():
    """check no files has conflicts"""
    return len(get_not_resolved_files(staged=True)) == 0


def get_modified_files():
    """get working area files"""
    output = subprocess.check_output(["git", "diff", "--name-only"], encoding='utf-8').strip()
    if output:
        return output.split('\n')
    return []


def check_need_push():
    """check if there are commits to be pushed"""
    try:
        output = subprocess.check_output(["git", "log", '--oneline', "@{u}.."], encoding='utf-8').strip()
        if output:
            return len(output.split('\n')) != 0
        return False
    except CalledProcessError:
        err('remote branch not setup yet, skipping check...')
        return True


def get_staged_files():
    """get files in staging area"""
    output = subprocess.check_output(["git", "diff", "--name-only", "--cached"], encoding='utf-8').strip()
    if output:
        return output.split('\n')
    return []


def reset_working_area():
    """restore working area"""
    return subprocess.check_output(["git", "restore", "."], encoding='utf-8').strip()


def add_new_changes():
    """git add additional changes"""
    return subprocess.check_output(["git", "add", "."], encoding='utf-8').strip()


class GitHelper:
    """Git helper to be used in various hooks"""

    def __init__(self):
        self.modified_files = get_modified_files()
        self.staged_files = get_staged_files()
        self.staged_files = filter_by_hooks_ignore(self.staged_files)
        self.staged_files = filter_by_existence(self.staged_files)

    def evaluate_hook_result(self, hook_result: bool):
        """
        Evaluate function result `hook_result` and either:
        - Exit program with exit code 1
        - Add new changes to staging area (if available)

        hook_result: False => exit(1)
        hooks_result: True => add modified changes and continue
        """
        if not hook_result:
            err("Errors encountered while hooks is running! Aborting commit...")
            reset_working_area()
            self.pop_stash()
            exit(1)
        modified_files = get_modified_files()
        if modified_files:
            add_new_changes()

    def stash(self):
        """stash files"""
        if self.modified_files:
            info("modified files detected! stashing...")
            subprocess.run(["git", "stash", "--include-untracked", "--keep-index", "-q"])

    def pop_stash(self):
        """pop stash"""
        if self.modified_files:
            info("Restoring modified files...")
            subprocess.run(["git", "stash", "pop", "-q"])

    def status(self):
        """list status"""
        if self.modified_files:
            subprocess.run(["git", "status"])
