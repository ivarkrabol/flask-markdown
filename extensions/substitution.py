import re
from typing import List, Pattern

from markdown import Markdown
from markdown.extensions import Extension
from markdown.postprocessors import Postprocessor


class SubstitutionExtension(Extension):
    def __init__(self):
        super().__init__()
        self._context_substitution: _ContextSubstitutionPreprocessor = None

    def extendMarkdown(self, md: Markdown, md_globals: dict) -> None:
        self._context_substitution = _ContextSubstitutionPreprocessor(md)
        md.postprocessors.add('context', self._context_substitution, '_end')
        md.postprocessors.add('special_characters', _SpecialCharacterSubstitutionPreprocessor(md, {
            '--': 'ndash'
        }), '_end')

    def set_context(self, context: dict) -> None:
        if self._context_substitution is not None:
            self._context_substitution.set_substitutions(context)


class _SubstitutionPreprocessor(Postprocessor):
    def __init__(self, markdown_instance: Markdown):
        super().__init__(markdown_instance)
        self._substitutions: dict = {}
        self._any_pattern: Pattern = None

    def run(self, text: str) -> str:
        if self._substitutions is None:
            return text
        return self._any_pattern.sub(lambda m: self._substitutions[m.group(1)], text)

    def set_substitutions(self, substitutions: dict) -> None:
        self._substitutions = substitutions
        self._any_pattern = self._pattern_from_substitutions() if substitutions is not None else None

    def _pattern_from_substitutions(self) -> Pattern:
        return re.compile(r'(' + '|'.join(map(re.escape, self._substitutions.keys())) + r')')


class _ContextSubstitutionPreprocessor(_SubstitutionPreprocessor):
    def _pattern_from_substitutions(self) -> Pattern:
        return re.compile(r'\{\{(' + '|'.join(map(re.escape, self._substitutions.keys())) + r')\}\}')


class _SpecialCharacterSubstitutionPreprocessor(_SubstitutionPreprocessor):
    def __init__(self, markdown_instance: Markdown, substitutions: dict):
        super().__init__(markdown_instance)
        self.set_substitutions({k: '&{};'.format(v) for k, v in substitutions.items()})