#!/usr/bin/env python3
from utils import make_sudo
from utils import run_cmd
#pull
is_root = make_sudo()
c1 = run_cmd("rm -rf '__pycache__'")
c2 = run_cmd("rm -r *.log")
c3 = run_cmd("git pull")
c4 = run_cmd("git status")

print(c3)
print(c4)