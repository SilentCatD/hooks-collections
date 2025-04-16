class bcolors:
    """Define colors to be used in logger"""
    HEADER = '\033[95m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    OKBLUE = '\033[94m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def warn(msg):
    """print warning message"""
    print(f"{bcolors.WARNING}[WARN]: {msg}{bcolors.ENDC}")


def ok(msg):
    """print success message"""
    print(f"{bcolors.OKGREEN}[SUCCESS]: {msg}{bcolors.ENDC}")


def err(msg):
    """print error message"""
    print(f"{bcolors.FAIL}[ERROR]: {msg}{bcolors.ENDC}")


def info(msg):
    """print info message"""
    print(f"{bcolors.OKBLUE}[INFO]: {msg}{bcolors.ENDC}")
