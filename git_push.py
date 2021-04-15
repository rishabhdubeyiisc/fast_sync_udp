#!/usr/bin/env python3
import sys
from utils import make_sudo
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

is_sudo = make_sudo()

s0 = run_cmd("chmod +x *.py")
s1 = run_cmd("rm -r *.log")
s2 = run_cmd("rm -rf '__pycache__'")
s3 = run_cmd("chown rishabhd:rishabhd *.py")
print(f" {s0} \n {s1} \n {s2} \n {s3} ")

commit_msg = sys.argv[1]
print("committing : {} ".format(commit_msg))
commit_msg = "'"+ str(commit_msg) +"'" 

c0 = run_cmd("git add .")
c1 = run_cmd("git commit -m " + str(commit_msg) )
c2 = run_cmd("git push")
print(f" {c0} \n {c1} \n {c2} ")