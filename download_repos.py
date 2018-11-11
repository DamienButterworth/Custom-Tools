#!/usr/bin/python

import os
import subprocess

path = os.getcwd()

repo_org_name = ""

repo_names = []


def git(*args):
    return subprocess.check_call(['git'] + list(args))


def clone():
    for repo in repo_names:
        if not (os.path.exists(os.path.join(path, repo))):
            git("clone", "git@github.com:/" + repo_org_name + "/" + repo + ".git")
        else:
            print("Folder already exists")