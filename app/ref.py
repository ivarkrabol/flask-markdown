import re
from typing import Callable

from app.md import MdLoader, Md

ANCHOR_PATTERN_STR = r'^\[([a-z:.]+)]:<>$'


class Refs:
    ANCHOR_PATTERN = re.compile(ANCHOR_PATTERN_STR)

    def __init__(self, md_loader: MdLoader):
        self._md_loader = md_loader
        self._searched_paths = []
        self._refs_cache = {}
        self.build_cache()

    def _add_to_searched_paths(self, request_path: str) -> None:
        self._searched_paths.append(request_path)

    def _add_to_refs_cache(self, ref: str, request_path: str) -> None:
        self._refs_cache[ref] = request_path

    def _file_resolve(self, request_path: str) -> None:
        self._resolved_path = request_path

    def build_cache(self) -> None:
        self._md_loader.for_each_file(
            _FileConsumer(self._add_to_refs_cache),
            self._searched_paths
        )

    def find(self, anchor: str) -> str:
        if anchor not in self._refs_cache:
            raise RefNotFound(anchor)
        return self._refs_cache[anchor]


class RefNotFound(Exception):
    pass


class _FileConsumer(Callable[[str, Md], bool]):
    def __init__(self, add_to_refs_cache: Callable[[str, str], None]):
        self.add_to_refs_cache = add_to_refs_cache

    def __call__(self, request_path: str, md: Md) -> bool:
        anchor_match = md.get_anchor_match(Refs.ANCHOR_PATTERN)
        if anchor_match and anchor_match.group(1):
            self.add_to_refs_cache(anchor_match.group(1), request_path)
        md.for_each_line(_LineConsumer(request_path, self.add_to_refs_cache), True)
        return True


class _LineConsumer(Callable[[str], bool]):
    def __init__(self, request_path: str, add_to_refs_cache: Callable[[str, str], None]):
        self.request_path = request_path
        self.add_to_refs_cache = add_to_refs_cache

    def __call__(self, line: str) -> bool:
        for anchor in re.findall(Refs.ANCHOR_PATTERN, line):
            self.add_to_refs_cache(anchor, '{}#{}'.format(self.request_path, anchor))
        return True
