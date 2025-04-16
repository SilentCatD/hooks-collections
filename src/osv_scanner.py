import os.path
import subprocess
from src.printer import info
import urllib.request
import tempfile
import shutil

osv_scanner_version = '2.1.0'

osv_scaner_temp_dir = 'osv_scanner_temp_installation_dir'

osv_scanner_file_name = f'osv-scanner_darwin_arm64'

exe_name = 'osv_scanner'



def osv_scanner_tempdir_path():
    """get temporary directory to install or execute gitleaks"""
    system_temp_dir = tempfile.gettempdir()
    temp_dir_path = os.path.join(system_temp_dir, osv_scaner_temp_dir)
    return temp_dir_path


def osv_installed() -> bool:
    """check gitleaks downloaded to temporary directory"""
    temp_dir_path = osv_scanner_tempdir_path()
    return os.path.exists(os.path.join(temp_dir_path, exe_name))


def install_osv_scanner():
    """download gitleaks if not yet"""
    if osv_installed():
        return
    temp_dir_path = osv_scanner_tempdir_path()
    os.makedirs(temp_dir_path, exist_ok=True)

    with open(os.path.join(temp_dir_path, exe_name), 'wb') as f:
        info("downloading osv scanner....")
        with urllib.request.urlopen(
                f'https://github.com/google/osv-scanner/releases/download/v2.0.1/osv-scanner_darwin_arm64') as df:
            f.write(df.read())

    os.chmod(os.path.join(temp_dir_path, exe_name), 0o755)

    info("osv scanner installed! (temporarily)")


def no_vulns() -> bool:
    """execute osv scanner to identify vuln"""
    if not osv_installed():
        install_osv_scanner()
    else:
        info("found cached osv scanner installation, skip downloading...")

    temp_dir_path = osv_scanner_tempdir_path()
    args = [str(os.path.join(temp_dir_path, exe_name))]

    args.extend(['scan', 'source', '.'])

    info(' '.join(args))
    run_result = subprocess.run(args)
    if run_result.returncode != 0:
        return False
    return True


def clean_up_osv_scanner():
    """remove osv scanner related artifact"""
    scanner_temp_dir = osv_scanner_tempdir_path()
    shutil.rmtree(scanner_temp_dir, ignore_errors=True)
    pass
