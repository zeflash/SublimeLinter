# jshint.py - sublimelint package for checking Javascript files

import json
import os
import os.path
import subprocess
import sublime

from utils import get_startupinfo

__all__ = ['run', 'language']
language = 'JavaScript'
description =\
'''* view.run_command("lint", "JavaScript")
        Turns background linter off and runs the JSHint linter
        (jshint, assumed to be on $PATH) on current view.
'''


def jshint_path():
    return os.path.join(os.path.dirname(__file__), 'libs', 'jshint.js')


def is_enabled():
    try:
        process = subprocess.Popen(jshint_path(), startupinfo=get_startupinfo())
        process.communicate('')
    except OSError as (errno, message):
        return (False, 'Cannot find or execute "{0}"'.format(jshint_path()))

    return (True, '')


def check(codeString):
    process = subprocess.Popen(jshint_path(),
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                startupinfo=get_startupinfo())

    result = process.communicate(codeString)[0]
    return json.loads(result)


def run(code, view, filename=None):
    try:
        errors = check(code)
    except OSError as (errno, message):
        print 'SublimeLinter: error executing linter: {0}'.format(message)
        errors = []

    lines = set()
    underlines = []
    errorMessages = {}

    def addMessage(lineno, message):
        if lineno in errorMessages:
            errorMessages[lineno].append(message)
        else:
            errorMessages[lineno] = [message]

    def underlineRange(lineno, position, length=1):
        line = view.full_line(view.text_point(lineno, 0))
        position += line.begin()

        for i in xrange(length):
            underlines.append(sublime.Region(position + i))

    for error in errors:
        lineno = error['line'] - 1  # jshint uses one-based line numbers
        lines.add(lineno)

        # Remove trailing period from error message
        reason = error['reason']

        if reason[-1] == '.':
            reason = reason[:-1]

        addMessage(lineno, reason)
        underlineRange(lineno, error['character'] - 1)

    return lines, underlines, [], [], errorMessages, {}, {}
