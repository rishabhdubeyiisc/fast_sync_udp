#!/usr/bin/env python3
import sys
from utils import check_sudo
from utils import run_cmd

def usage():
    print("please add up commit msg")
    print("To set config    : pass True as second argument")
    print("example          : 'This is my commit msg' 'init'")

if (len(sys.argv) < 2 ):
    usage()
    exit(-1)

if (len(sys.argv) > 2):
    if (sys.argv[2] == 'init'):
        run_cmd('git config --global user.email "rishidd7devx2@gmail.com"')
        run_cmd('git config --global user.name "rishabhdubeyiisc"')

is_sudo = check_sudo()

commit_msg = sys.argv[1]
print("committing : {} ".format(commit_msg))
commit_msg = "'"+ str(commit_msg) +"'" 

run_cmd("rm -r *.log")
run_cmd("rm -rf '__pycache__'")
run_cmd("git add .")
run_cmd("git commit -m " + str(commit_msg) )
run_cmd("git push")