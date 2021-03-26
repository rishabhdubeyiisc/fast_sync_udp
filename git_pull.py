#!/usr/bin/env python3
from utils import make_sudo
from utils import run_cmd

is_root = make_sudo()
run_cmd("rm -rf '__pycache__'")
run_cmd("rm -r *.log")
run_cmd("git pull")
run_cmd("git status")