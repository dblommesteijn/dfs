

class Config(object):

    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state

    def set_parser(self, parser):
        (self._args, self._opts) = parser.parse_args()

    def get_opts(self):
        return self._opts

    def get_args(self):
        return self._args

