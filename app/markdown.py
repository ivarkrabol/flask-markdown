from markdown import Markdown as _Markdown

from app.ref import Refs
from extensions import AnchorExtension, BootstrapifyExtension, FormatHrefsExtension, StructureExtension, \
    SubstitutionExtension


class Markdown:
    def __init__(self, refs: Refs):
        self._substitution_extension: SubstitutionExtension = SubstitutionExtension()

        self._markdown: _Markdown = _Markdown(extensions=[
            'markdown.extensions.tables',
            AnchorExtension(refs),
            BootstrapifyExtension(),
            FormatHrefsExtension(),
            StructureExtension(),
            self._substitution_extension,
        ])

    def convert(self, content: str, context: dict = None) -> str:
        self._substitution_extension.set_context(context)
        return self._markdown.convert(content)
