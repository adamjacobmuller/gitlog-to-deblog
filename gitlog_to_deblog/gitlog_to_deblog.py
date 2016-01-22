#!/usr/bin/python2.7
import sh
import re
import sys
import datetime

from pygit2 import Repository
from pygit2 import GIT_SORT_TOPOLOGICAL, GIT_SORT_REVERSE
from sh import git


def main():
    package = sys.argv[1]

    repo = Repository('.git')

    stripv = re.compile("v(\d+\.\d+\.\d+.*)")

    checktag = True

    log = """{package} ({version}) unstable; urgency=low

  * {message}

 -- {author_name} <{author_email}>  {time}
"""
    for commit in repo.walk(repo.head.target, GIT_SORT_TOPOLOGICAL):
        if checktag:
            try:
                version = git("describe", "--tags", commit.id).strip()
            except sh.ErrorReturnCode_128:
                version = '0.0.0-0-g%s' % str(commit.id)[0:7]
                checktag = False
        else:
            version = '0.0.0-0-g%s' % str(commit.id)[0:7]

        stripr = stripv.search(version)
        if stripr is not None:
            version = stripr.group(1)
        message = commit.message.encode("ascii", errors="replace").strip()
        messages = ["  %s" % line for line in message.split("\n")]
        messages[0] = messages[0].strip()
        message = "\n".join(messages)
        print log.format(**dict(
            package=package,
            version=version,
            message=message,
            author_name=commit.author.name.encode("ascii", errors="replace"),
            author_email=commit.author.email.encode("ascii", errors="replace"),
            time=datetime.datetime.fromtimestamp(commit.commit_time).strftime("%a, %d %b %Y %H:%M:%S -0000")
        ))
