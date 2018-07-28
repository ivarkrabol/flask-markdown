import os


class MdLoader:
    def __init__(self):
        self.base_path = os.path.abspath('md')
        self.cached = {}

    def get(self, request_path):
        if request_path in self.cached:
            return self.cached[request_path]
        md_path = os.path.normpath(os.path.join(self.base_path, '{}.md'.format(request_path)))
        if md_path in self.cached:
            self.cached[request_path] = self.cached[md_path]
            return self.cached[md_path]
        if not md_path.startswith(self.base_path):
            raise IllegalPath(request_path)
        if not os.path.isfile(md_path):
            print(md_path)
            raise NoMdAtPath(request_path)
        md = Md(md_path)
        self.cached[request_path] = md
        self.cached[md_path] = md
        return md


class IllegalPath(Exception):
    pass


class NoMdAtPath(Exception):
    pass


class Md:
    def __init__(self, path):
        self.path = path

    def do(self, line_func):
        file = open(self.path, 'r')
        map(line_func, file)
        file.close()

    def read(self):
        file = open(self.path, 'r')
        file_dump = file.read()
        file.close()
        return file_dump
