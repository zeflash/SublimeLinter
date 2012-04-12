# -*- coding: utf-8 -*-
# css.py - sublimelint package for checking CSS files

import os
import json

from base_linter import BaseLinter

CONFIG = {
    'language': 'CSS'
}


class Linter(BaseLinter):
    def __init__(self, config):
        super(Linter, self).__init__(config)
        self.use_jsc = False

    def get_executable(self, view):
        foundEngine, path, message = self.get_javascript_engine(view)
        self.use_jsc = path == self.jsc_path()
        self.js_engine = os.path.join(self.js_engine_path(), 'jsc.js' if self.use_jsc else 'node.js')
        return (foundEngine, path, message)

    def get_lint_args(self, view, code, filename):
        path = self.csslint_path()
        options = json.dumps(view.settings().get("csslint_options") or {})

        if self.use_jsc:
            args = (self.js_engine, '--', path + os.path.sep, str(code.count('\n')), options)
        else:
            args = (self.js_engine, path + os.path.sep, options)

        return args

    def csslint_path(self):
        return os.path.join(os.path.dirname(__file__), 'libs', 'csslint')

    def parse_errors(self, view, errors, lines, errorUnderlines, violationUnderlines, warningUnderlines, errorMessages, violationMessages, warningMessages):
        errors = json.loads(errors.strip() or '[]')

        for error in errors:
            lineno = error['line']

            if error['type'] == 'warning':
                messages = warningMessages
                underlines = warningUnderlines
            else:
                messages = errorMessages
                underlines = errorUnderlines

            self.add_message(lineno, lines, error['reason'], messages)
            self.underline_range(view, lineno, error['character'] - 1, underlines)
