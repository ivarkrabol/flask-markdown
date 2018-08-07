import os
from typing import Callable, Pattern, Match


class Md:
    def __init__(self, path: str):
        self._path: str = path

    def for_each_line(self, func: Callable[[str], bool], skip_first: bool = False) -> None:
        file = open(self._path, 'r')
        if skip_first:
            file.readline()
        for line in file:
            if not func(line):
                break
        file.close()

    def read(self) -> str:
        file = open(self._path, 'r')
        file_dump = file.read()
        file.close()
        return file_dump

    def get_anchor_match(self, pattern: Pattern) -> Match:
        file = open(self._path, 'r')
        match = pattern.match(file.readline())
        file.close()
        return match


class MdLoader:
    def __init__(self):
        self._base_path = os.path.abspath('md')
        self._cached = {}

    def get(self, request_path: str) -> Md:
        if request_path in self._cached:
            return self._cached[request_path]
        md_path = os.path.normpath(
            os.path.join(self._base_path, '{}.md'.format(request_path).replace('/.md', '/index.md')))
        if md_path in self._cached:
            self._cached[request_path] = self._cached[md_path]
            return self._cached[md_path]
        if not md_path.startswith(self._base_path):
            raise IllegalPath(request_path)
        if not os.path.isfile(md_path):
            raise NoMdAtPath(request_path)
        md = Md(md_path)
        self._cached[request_path] = md
        self._cached[md_path] = md
        return md

    def for_each_file(self, func: Callable[[str, Md], bool], excluding: list = None) -> None:
        for dir_path, _, filenames in os.walk(self._base_path):
            for filename in filenames:
                if not filename.endswith('.md'):
                    continue
                request_path = os.path.relpath(os.path.join(dir_path, filename[:-3]), self._base_path)
                if excluding and request_path in excluding:
                    continue
                if not func(request_path, self.get(request_path)):
                    return


class IllegalPath(Exception):
    pass


class NoMdAtPath(Exception):
    pass
