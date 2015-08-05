from dfs.common import FileDir, Helper, Reflect


class Cmd(object):

    def __init__(self):
        self._errors = []
        self._cmds = {}
        self._cmd = None
        # find cmd pyfiles and initialize them
        current_dir = FileDir.get_current_dir_of_file(__file__)
        py_files = FileDir.get_py_files_in_dir(current_dir + "/cmds")
        classes = Reflect.get_classes_by_files(py_files, "dfs.cmds")
        for clazz in classes:
            c = clazz()
            if c.is_enabled():
                self._cmds[clazz.__name__.lower()] = c

    def set_opt(self, opt):
        if not opt in self._cmds:
            return
        self._opt = opt
        self._cmd = self._cmds[self._opt]

    def get_help(self):
        return "\r\n".join([c.get_help() for k,c in self._cmds.iteritems()])

    def validate(self):
        self._cmd.validate()
        if self._cmd.has_errors():
            self._errors.append(self._cmd.get_errors_str())

    def invalid_cmd(self):
        return self._cmd == None

    def has_errors(self):
        return len(self._errors) > 0

    def get_errors_str(self):
        return ",".join(self._errors)

    def run(self):
        self._cmd.run()


# if opts[0] == "init":
    #     from dfs.cmds.init import Init
    #     init = Init(opts[1:])
    #     if init.has_errors():
    #         print "dfs: " + init.get_errors_str()
    #         sys.exit(-1)
    #     init.run()
    # elif: opts[0] == "add":
    #     from dfs.cmds.add import Add
    #     add = Add(opts[1:])
    # else:
    #     print "dfs: undefined option (try -h)"
    #     sys.exit(-1)