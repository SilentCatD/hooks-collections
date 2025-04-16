import os.path
import subprocess
from src.printer import info
import urllib.request
import tempfile
import tarfile
import shutil

from src.utils import is_in_ci

gitleaks_version = '8.23.3'

gitleaks_temp_dir = 'gitleaks_temp_installation_dir'

tar_file_name = f'gitleaks_{gitleaks_version}_darwin_arm64.tar.gz'

gitleaks_file_name = 'gitleaks'

gitleaks_config_file_name = '.gitleaks.toml'

gitleaks_report_file_name = 'gitleaks_findings.json'


def gitleaks_tempdir_path():
    """get temporary directory to install or execute gitleaks"""
    system_temp_dir = tempfile.gettempdir()
    temp_dir_path = os.path.join(system_temp_dir, gitleaks_temp_dir)
    return temp_dir_path


def gitleaks_installed() -> bool:
    """check gitleaks downloaded to temporary directory"""
    temp_dir_path = gitleaks_tempdir_path()
    return os.path.exists(os.path.join(temp_dir_path, gitleaks_file_name))


def install_gitleaks():
    """download gitleaks if not yet"""
    if gitleaks_installed():
        return
    temp_dir_path = gitleaks_tempdir_path()
    os.makedirs(temp_dir_path, exist_ok=True)

    with open(os.path.join(temp_dir_path, tar_file_name), 'wb') as f:
        info("downloading gitleaks....")
        with urllib.request.urlopen(
                f'https://github.com/gitleaks/gitleaks/releases/download/v{gitleaks_version}/{tar_file_name}') as df:
            f.write(df.read())

    with tarfile.open(os.path.join(temp_dir_path, tar_file_name), 'r') as f:
        info("extracting....")
        f.extractall(path=temp_dir_path)

    os.chmod(os.path.join(temp_dir_path, gitleaks_file_name), 0o755)

    info("gitleaks installed! (temporarily)")


def no_leaks(files: list[str] = None) -> bool:
    """execute gitleaks to identify leakages"""
    temp_dir_path = gitleaks_tempdir_path()
    if not gitleaks_installed():
        install_gitleaks()
    else:
        info("found cached gitleaks installation, skip downloading...")

    args = [str(os.path.join(temp_dir_path, gitleaks_file_name)), 'dir']

    if not is_in_ci():
        args.append('-v')

    has_config_file = os.path.exists(os.path.join(os.curdir, gitleaks_config_file_name))

    if files:
        args.extend(files)

    if has_config_file:
        args.extend(['--config', gitleaks_config_file_name])

    args.extend(['--report-path', gitleaks_report_file_name])

    info(' '.join(args))
    run_result = subprocess.run(args)
    if run_result.returncode != 0:
        return False
    return True


def clean_up_gitleaks():
    """remove gitleaks related artifact"""
    git_leak_temp_dir = gitleaks_tempdir_path()
    shutil.rmtree(git_leak_temp_dir, ignore_errors=True)
    pass
