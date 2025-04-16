import os.path
import shutil

from src.git_helper import get_git_root_dir


class VenvManager:
    def __init__(self, env_name='mobile_env'):
        self.env_name = env_name
        self.path = f'.git/hooks/{self.env_name}'
        self.path = os.path.join(get_git_root_dir(), self.path)

    def create(self):
        os.system(f'python3 -m venv {self.path}')

    def exist(self):
        return os.path.exists(self.path)

    def create_if_not_exist(self):
        if not self.exist():
            self.create()

    def clean_up(self):
        shutil.rmtree(self.path, ignore_errors=True)

    def install_package(self):
        self.create_if_not_exist()
        requirements_file = 'requirements.txt'
        if not os.path.exists(requirements_file):
            return
        os.system(f'. {self.path}/bin/activate && pip install -r {requirements_file} && deactivate')
