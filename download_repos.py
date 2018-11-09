#!/usr/bin/python

import os, shutil, subprocess

#location of cloned files
path = ""

#organisation associated
repo_org_name = ""

#repo name list
file = open("data.txt")

repos = file.readlines()


def git(*args):
    return subprocess.check_call(['git'] + list(args))

def clone():
    for repo in repos:
        if not (os.path.exists(path + "/" + repo.replace('\n', ""))):  
            git("clone", repo_org_name + repo.replace('\n', "") + ".git")
        else:
            print("Folder already exists")

os.chdir(path)
clone()
