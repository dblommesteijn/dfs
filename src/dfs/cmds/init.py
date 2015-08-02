
from dfs.config import Config

import os

class Init(object):

    def __init__(self, opts):
        self._config = Config()
        self._opts = opts
        self._errors = []
        if len(self._opts) != 2:
            self._errors.append("no target and size provided (try -h)")
            return
        self._target = self._opts[0]
        self._size = int(self._opts[1])
        f = self._config.get_args().force
        # check if target it not a directory
        if os.path.isdir(self._target):
            self._errors.append("target is a directory, quitting")
            return
        # check if target does not exist
        if os.path.isfile(self._target) and not f:
            self._errors.append("target exists (-f to overwrite)")
            return
        # check if path to file exists
        dirname = os.path.dirname(self._target)
        if not os.path.isdir(dirname):
            self._errors.append("target directory does not exist, quitting")
            return

    def has_errors(self):
        return len(self._errors) > 0

    def get_errors_str(self):
        return ",".join(self._errors)

    def run(self):
        fd = os.open(self._target, os.O_RDWR|os.O_CREAT)
        # input offset megabites
        os.ftruncate(fd, self._size * 1000000)
        os.close(fd)


