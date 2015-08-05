import os, glob, re, inspect

class FileDir(object):

    @classmethod
    def get_current_dir_of_file(cls, file):
        return os.path.dirname(os.path.abspath(__file__))

    @classmethod
    def get_py_files_in_dir(cls, base_dir):
        return glob.glob("%s/*.py" % (base_dir))


class Helper(object):

    @classmethod
    def underscore_to_lower_camelcase(cls, underscore):
        cc = re.sub('(?!^)[_]', '', underscore.title())
        return cc[0].lower() + cc[1:]

    @classmethod
    def underscore_to_upper_camelcase(cls, underscore):
        return re.sub('(?!^)[_]', '', underscore.title())

    @classmethod
    def camelcase_to_underscore(cls, camelcase):
        return re.sub('(?!^)([A-Z]+)', r'_\1',camelcase).lower()

    @classmethod
    def is_camelcase(cls, value):
        return re.match(r'[A-Z]', value) != None

    @classmethod
    def is_underscore(cls, input):
        return re.match(r'[_]', value) != None

class Reflect(object):

    @classmethod
    def get_classes_by_files(cls, files, prefix):
        """Get classes by python files, mapping on py_module: PyClass
        Parameters:
          files - a list of python files (with abs)
          pefix - module namespace prefix
        Return:
          array of classes
        """
        classes = []
        for file in files:
            name = os.path.basename(os.path.splitext(file)[0])
            # import module based on offset
            module = __import__(("%s.%s" % (prefix, name)),
                globals(), locals(), [name.title()], -1)
            if module == None:
                continue
            # import module members based on module name
            lookup = inspect.getmembers(module, inspect.isclass)
            if len(lookup) <= 0:
                continue
            clazz = None
            for l in lookup:
                if l[1].__name__ == Helper.underscore_to_upper_camelcase(name):
                    clazz = l[1]
                    break
            if clazz == None:
                continue
            classes.append(clazz)
        return classes

