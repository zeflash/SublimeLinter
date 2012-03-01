# -*- coding: utf-8 -*-
# perlcritic.py - sublimelint package for checking perl files

import re
#import subprocess

from base_linter import BaseLinter

CONFIG = {
    'language': 'perlcritic',
    'executable': 'perlcritic',
    'test_existence_args': '--version',
    'lint_args': '{filename}',
    'input_method': 3,
}


class Linter(BaseLinter):
    def parse_errors_perl(self, view, errors, lines, errorUnderlines, violationUnderlines, warningUnderlines, errorMessages, violationMessages, warningMessages):
        for line in errors.splitlines():
            match = re.match(r'(?P<error>.+?) at .+? line (?P<line>\d+)(, near "(?P<near>.+?)")?', line)

            if match:
                error, line = match.group('error'), match.group('line')
                lineno = int(line)
                near = match.group('near')

                if near:
                    error = '{0}, near "{1}"'.format(error, near)
                    self.underline_regex(view, lineno, '(?P<underline>{0})'.format(re.escape(near)), lines, errorUnderlines)

                self.add_message(lineno, lines, error, errorMessages)

    def underline_word(self, view, lineno, position, underlines):
        # Assume lineno is one-based, ST2 wants zero-based line numbers
        lineno -= 1
        line = view.full_line(view.text_point(lineno, 0))
        position += line.begin()

        word = view.word(position)
        underlines.append(word)

    def parse_errors(self, view, errors, lines, errorUnderlines, violationUnderlines, warningUnderlines, errorMessages, violationMessages, warningMessages):
        for line in errors.splitlines():
            # I like to see these errors in the console
            print(line)
            match = re.match(r'\[(?P<pbp>.+)\] (?P<error>.+?) at line (?P<line>\d+), column (?P<column>\d+).+?', line)

            if match:
                error, line, column = match.group('error'), match.group('line'), match.group('column')
                lineno = int(line)
                column = int(column) - 1

                self.add_message(lineno, lines, error, errorMessages)
                self.underline_word(view, lineno, column, errorUnderlines)
