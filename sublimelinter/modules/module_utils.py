import os
import subprocess


def get_startupinfo():
    info = None

    if os.name == 'nt':
        info = subprocess.STARTUPINFO()
        info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        info.wShowWindow = subprocess.SW_HIDE

    return info


def execute_get_output(args):
    try:
        return subprocess.Popen(args, get_startupinfo()).communicate()[0]
    except:
        return ''
