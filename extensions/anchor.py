import re
from typing import List, Match

from markdown import Markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.util import etree

from app.ref import Refs, ANCHOR_PATTERN_STR, RefNotFound


class AnchorExtension(Extension):
    def __init__(self, refs: Refs):
        super().__init__()
        self.refs = refs

    def extendMarkdown(self, md: Markdown, md_globals: dict):
        md.preprocessors.add('ref', RefPreprocessor(md, self.refs), '_begin')
        md.preprocessors.add('anchor', AnchorPreprocessor(md), '>ref')


class RefPreprocessor(Preprocessor):
    def __init__(self, markdown_instance: Markdown, refs: Refs):
        super().__init__(markdown_instance)
        self.pattern = re.compile(r'\[[^]]+?]\(!([a-z:.]+)\)')
        self.refs = refs

    def run(self, lines: List[str]) -> List[str]:
        new_lines = []
        for line in lines:
            m = self.pattern.search(line)
            while m:
                line = line[:m.start()] + self.match_replacement(m) + line[m.end():]
                m = self.pattern.search(line, m.start() + 1)
            new_lines.append(line)
        return new_lines

    def match_replacement(self, m: Match) -> str:
        m_all = m.group(0)
        offset = m.start()
        anchor = m.group(1)

        try:
            href = '/{}'.format(self.refs.find(anchor))
        except RefNotFound as err:
            print('RefNotFound: {}'.format(err))
            href = '/{}'.format(anchor)

        return m_all[:(m.start(1) - offset - 1)] + href + m_all[(m.end(1) - offset):]


class AnchorPreprocessor(Preprocessor):
    def __init__(self, markdown_instance: Markdown):
        super().__init__(markdown_instance)
        self.pattern = re.compile(ANCHOR_PATTERN_STR)

    def run(self, lines: List[str]) -> List[str]:
        new_lines = []
        i = 0
        while i < len(lines):
            new_lines.append(lines[i])
            m = self.pattern.match(lines[i])
            i += 1
            if m:
                new_lines.append(etree.tostring(etree.Element('a', {'name': m.group(1)}), encoding='unicode'))
                while len(lines[i].strip()) == 0 and i < len(lines):
                    i += 1

        return new_lines
