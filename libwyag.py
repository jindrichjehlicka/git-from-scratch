import argparse
import configparser
from datetime import datetime

# users/group DB on unix
import grp, pwd

# match filenames
from fnmatch import fnmatch

from math import ceil

import os

import re

import sys  # access command line args

import zlib  # git compresses with zlib


argparser = argparse.ArgumentParser(descriptions='Jay"s content tracker')

argsubparsers = argparser.add_subparsers(title="Command", dest="command")
argsubparsers.required = True


def main(argsv=sys.argv[1:]):
    args = argparser.parse_args(argsv)

    match args.command:
        # case "add":
        #     cmd_add(args)
        # case "cat-file":
        #     cmd_cat_file(args)
        # case "check-ignore":
        #     cmd_check_ignore(args)
        # case "checkout":
        #     cmd_checkout(args)
        # case "commit":
        #     cmd_commit(args)
        # case "hash-object":
        #     cmd_hash_object(args)
        case "init":
            cmd_init(args)
        # case "log":
        #     cmd_log(args)
        # case "ls-files":
        #     cmd_ls_files(args)
        # case "ls-tree":
        #     cmd_ls_tree(args)
        # case "rev-parse":
        #     cmd_rev_parse(args)
        # case "rm":
        #     cmd_rm(args)
        # case "show-ref":
        #     cmd_show_ref(args)
        # case "status":
        #     cmd_status(args)
        # case "tag":
        #     cmd_tag(args)
        # case _:
        #     print("Bad command.")



class GitRepository (object):
    """A git repository"""
    
    worktree = None
    gitdir = None
    conf = None
    
    def __init__(self, path, force=False) -> None:
        self.worktree = path
        self.gitdir = os.path.join(path, ".git")
        
        if not (force or os.path.isdir(self.gitdir)):
            raise Exception(f"Not a Git repository {path}")
        
        self.conf = configparser.ConfigParser()
        cf = repo_file(self, "config")
        
        if cf and os.path.exists(cf):
            self.conf.read([cf])
        elif not force:
            raise Exception("Configuration file missing")
        
        if not force:
            vers = int(self.conf.get("core", "repositoryformatversion"))
            if vers != 0:
                raise Exception("Unsupported repositoryformatversion: {vers}")
            
            
        # TODO: change repo to gitdir
        def repo_path(repo, *path):
            """Compute path for repo's gitdir"""
            return os.path.join(repo.gitdir, *path)

            
        def repo_file(repo, *path, mkdir =False):
            pass
            
