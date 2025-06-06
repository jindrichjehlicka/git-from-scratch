import argparse
import configparser
from datetime import datetime
from typing import Optional

# users/group DB on unix
import grp, pwd

# match filenames
from fnmatch import fnmatch

from math import ceil

import os

import re

import sys  # access command line args

import zlib  # git compresses with zlib


argparser = argparse.ArgumentParser(description='Jay"s content tracker')

argsubparsers = argparser.add_subparsers(title="Command", dest="command")
argsubparsers.required = True


argsp = argsubparsers.add_parser("init", help="Initialize a new, empty repository.")


def cmd_init(args):
    repo_create(args.path)


argsp.add_argument(
    "path",
    metavar="directory",
    nargs="?",
    default=".",
    help="Where to create the repository.",
)


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


class GitRepository(object):
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


def repo_path(repo, *path) -> str:
    """Compute path for repo's gitdir"""
    return os.path.join(repo.gitdir, *path)


def repo_file(repo, *path, mkdir=False) -> Optional[str]:
    if repo_dir(repo, *path[:-1], mkdir=mkdir):
        return repo_path(repo, *path)


def repo_dir(repo, *path, mkdir=False) -> Optional[str]:
    path = repo_path(repo, *path)

    if os.path.exists(path):
        if os.path.isdir(path):
            return path
        else:
            raise Exception(f"Not a directory {path}")

    if mkdir:
        os.makedirs(path)
        return path
    else:
        return None


def repo_create(path):
    """Create a new repository at path"""
    repo = GitRepository(path, True)

    if os.path.exists(repo.worktree):
        if not os.path.isdir(repo.worktree):
            raise Exception(f"{path} is not a directory!")
        if os.path.exists(repo.gitdir) and os.listdir(repo.gitdir):
            raise Exception(f"{path} it not empty!")
    else:
        os.makedirs(repo.worktree)

        assert repo_dir(repo, "branches", mkdir=True)
        assert repo_dir(repo, "objects", mkdir=True)
        assert repo_dir(repo, "refs", "tags", mkdir=True)
        assert repo_dir(repo, "refs", "heads", mkdir=True)

        # .git/description
        with open(repo_file(repo, "description"), "w") as f:
            f.write(
                "Unnamed repository; edit this file 'description' to name the repository.\n"
            )

        # .git/HEAD
        with open(repo_file(repo, "HEAD"), "w") as f:
            f.write("ref: refs/heads/master\n")

        with open(repo_file(repo, "config"), "w") as f:
            config = repo_default_config()
            config.write(f)

        return repo


def repo_default_config():
    ret = configparser.ConfigParser()

    ret.add_section("core")
    ret.set("core", "repositoryformatversion", "0")
    ret.set("core", "filemode", "false")
    ret.set("core", "bare", "false")

    return ret


def repo_find(path=".", required=True):
    path = os.path.realpath(path)

    if os.path.isdir(os.path.join(path, ".git")):
        return GitRepository(path)

    # if we havent returned, recurse in parent
    parent = os.path.realpath(os.path.join(path, ".."))
    if parent == path:
        if required:
            raise Exception("No git repository")
        else:
            return None
    return repo_find(parent, required)

# Generic class
class GitObject(object):

    def __init__(self, data=None):
        if data != None:
            self.deserialize(data)
        else:
            self.init()

    def deserialize(self, repo):
        raise Exception("Not Implemented!")

    def serialize(self, data):
        raise Exception("Not implemented!")

    def init (self):
        pass
    
    