"""Explicit installer and portable interpreter selector; never installs on server start."""
import argparse
import os
from pathlib import Path
import subprocess
import sys
import venv

ROOT = Path(__file__).resolve().parent
ENV = ROOT / '.venv'
PYTHON = ENV / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['install','run'])
    args,extra=parser.parse_known_args()
    if args.command=='install':
        if extra:parser.error('install accepts no additional arguments')
        if not ENV.exists():venv.EnvBuilder(with_pip=True).create(ENV)
        subprocess.run([str(PYTHON),'-m','pip','install','-r',str(ROOT/'requirements.txt')],check=True)
    else:
        if not PYTHON.is_file():parser.exit(2,'Run the explicit install command first. No installation occurs during startup.\n')
        os.execv(str(PYTHON),[str(PYTHON),str(ROOT/'server.py'),*extra])
