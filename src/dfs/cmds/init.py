
from dfs.config import Config

import os

class Init(object):

    def __init__(self, opts):
        self._config = Config()
        self._opts = opts
        self._errors = []
        target = self._opts[0]
        f = self._config.get_args().force
        if os.path.isfile(target) and not f:
            self._errors.append("target exists (-f to overwrite)")

    def has_errors(self):
        return len(self._errors) > 0

    def get_errors_str(self):
        return ",".join(self._errors)

    def run(self):
        pass


