import os
from typing import Callable, Pattern, Match


class Md:
    def __init__(self, path: str):
        self.path = path

    def for_each_line(self, func: Callable[[str], bool], skip_first: bool = False) -> None:
        file = open(self.path, 'r')
        if skip_first:
            file.readline()
        for line in file:
            if not func(line):
                break
        file.close()

    def read(self) -> str:
        file = open(self.path, 'r')
        file_dump = file.read()
        file.close()
        return file_dump

    def get_anchor_match(self, pattern: Pattern) -> Match:
        file = open(self.path, 'r')
        match = pattern.match(file.readline())
        file.close()
        return match


class MdLoader:
    def __init__(self):
        self.base_path = os.path.abspath('md')
        self.cached = {}

    def get(self, request_path: str) -> Md:
        if request_path in self.cached:
            return self.cached[request_path]
        md_path = os.path.normpath(
            os.path.join(self.base_path, '{}.md'.format(request_path).replace('/.md', '/index.md')))
        if md_path in self.cached:
            self.cached[request_path] = self.cached[md_path]
            return self.cached[md_path]
        if not md_path.startswith(self.base_path):
            raise IllegalPath(request_path)
        if not os.path.isfile(md_path):
            raise NoMdAtPath(request_path)
        md = Md(md_path)
        self.cached[request_path] = md
        self.cached[md_path] = md
        return md

    def for_each_file(self, func: Callable[[str, Md], bool], excluding: list = None) -> None:
        for dir_path, _, filenames in os.walk(self.base_path):
            for filename in filenames:
                request_path = os.path.relpath(os.path.join(dir_path, filename[:-3]), self.base_path)
                if excluding and request_path in excluding:
                    continue
                if not func(request_path, self.get(request_path)):
                    return


class IllegalPath(Exception):
    pass


class NoMdAtPath(Exception):
    pass
