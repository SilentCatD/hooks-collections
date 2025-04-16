from src.git_helper import get_git_diff
from src.ollama_interactor import generate_commit_message_body
from src.venv_manager import VenvManager
from src.printer import *

ok(
    generate_commit_message_body(get_git_diff(staged=False)))
