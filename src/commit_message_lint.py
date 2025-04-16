from src.printer import *
import re

convention_type = {
    "feat",
    "fix",
    "chore",
    "refactor",
    "docs",
    "style",
    "test",
    "perf",
    "ci",
    "build",
    "revert"
}


class CommitMessageLint:
    """
    Class implement set of pre-defined rules in commit-template.txt
    """

    def __init__(self, msg: str, file: str = None):
        # split msg by line
        # extract subject, type, scope from the msg
        self.file = file
        raw_msgs = msg.strip().split('\n')
        self.msg = []
        for line in raw_msgs:
            if not line.startswith("#"):
                self.msg.append(line)

        self.aborted = False
        if not self.msg or not self.msg[0]:
            self.aborted = True
            return
        if self.aborted:
            err("Title not found, aborted")
            exit(1)
        matched = re.search(r"^(?:(.+?)(?:\((.+?)\))?: *)?(.*)", self.msg[0], re.IGNORECASE)
        if not matched:
            warn("Commit message does not match any pattern")
        self.subject = matched.groups()[2]
        self.type = matched.groups()[0]
        self.scope = matched.groups()[1]

    def separate_subject_body_with_blank_lines(self):
        """Ensure space between title and body"""
        if self.aborted:
            return True
        if not self.msg or len(self.msg) <= 1:
            return True
        if self.msg[1] != '':
            warn("No line between subject and body\n"
                 "Rule #1: Separate subject from body with a blank line")
            return False
        return True

    def max_char_count_subject_line(self):
        """Ensure title max char"""
        if self.aborted:
            return True
        if len(self.msg[0]) > 50:
            warn("Subject length > 50 characters\n"
                 "Rule #2: Limit the subject line to 50 characters")
            return False
        return True

    def capitalize_first_subject_char(self):
        """Ensure first char of subject is uppercase"""
        if self.aborted:
            return True
        if self.subject and not self.subject[0].isupper():
            warn("First subject character should be capitalized\n"
                 "Rule #3: Capitalize the first character of subject")
            return False
        return True

    def all_type_symbol_lowercase(self):
        """Ensure all type(scope) character is lowercase"""
        if self.aborted:
            return True
        strs = ""
        if self.type:
            strs += self.type
        if self.scope:
            strs += f"({self.scope})"

        if not strs:
            return True

        if not strs.islower():
            warn("Type and scope should be lowercase\n"
                 "Rule #4: All type(scope) symbol is lowercase\n"
                 f"{strs.lower()}")
            return False
        return True

    def subject_trailing_dot(self):
        """Ensure subject don't have trailing dot"""
        if self.aborted:
            return True
        if self.subject.rstrip().endswith('.'):
            warn("Subject ending with .\n"
                 "Rule #5: Do not end the subject line with a period")
            return False
        return True

    def body_wrapped(self):
        """Ensure msg body wrapped"""
        if self.aborted:
            return True
        if len(self.msg) <= 1:
            return True
        for line in self.msg[1:]:
            if len(line) > 72:
                warn("Body text is not wrapped at 72 character\n"
                     "Rule #7: Wrap the body at 72 characters\n"
                     f"#{len(line)} chars| {line} ")
                return False
        return True

    def should_use_type(self):
        """Ensure type(scope) in the msg"""
        if self.aborted:
            return True
        if not self.type or self.type not in convention_type:
            warn("Commit title should have type\n"
                 "Rule #9: Commit title should have a conventional type")
            return False
        return True

    def write_commit_msg(self):
        if self.aborted:
            return True
        if not self.file:
            return True
        with open(self.file, 'w+') as f:
            f.write('\n'.join(self.msg))
        return True
