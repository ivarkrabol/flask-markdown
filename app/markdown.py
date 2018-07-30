from markdown import Markdown as _Markdown

from extensions import AnchorExtension, NdashExtension, WrapperExtension, StripMdExtension, BootstrapifyExtension


class Markdown:
    def __init__(self, refs):
        self._markdown = _Markdown(extensions=[
            AnchorExtension(refs),
            NdashExtension(),
            WrapperExtension(),
            StripMdExtension(),
            BootstrapifyExtension(),
            'markdown.extensions.tables',
        ])

    def convert(self, content: str) -> str:
        return self._markdown.convert(content)
