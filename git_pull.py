#!/usr/bin/env python3
from utils import check_sudo
from utils import run_cmd

run_cmd("rm -rf '__pycache__'")
run_cmd("rm -r *.log")
run_cmd("git pull")
run_cmd("git status")