# -*- coding: utf-8 -*-
# lua.py - sublimelint package for checking lua files

import re
import subprocess
from base_linter import BaseLinter

CONFIG = {
    'language': 'lua',
    'lint_args': '-'
}


class Linter(BaseLinter):

    def parse_errors(self, view, errors, lines, errorUnderlines, violationUnderlines, warningUnderlines, errorMessages, violationMessages, warningMessages):
        for line in errors.splitlines():
            match = re.match(r'^.+:(?P<line>\d+):\s+(?P<error>.+)', line)

            if match:
                error, line = match.group('error'), match.group('line')
                self.add_message(int(line), lines, error, errorMessages)

    def get_executable(self, view):
        self.linter = view.settings().get('sublimelinter_executable_map').get('lua', 'luac')

        try:
            path = self.get_mapped_executable(view, self.linter)
            subprocess.call([path, '-v'], startupinfo=self.get_startupinfo())
            return (True, path, 'using {0}'.format(self.linter))
        except OSError:
            return (False, '', '{0} is required'.format('luac'))
