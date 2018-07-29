from markdown import Markdown as _Markdown

from extensions import AnchorExtension, NdashExtension, WrapperExtension


class Markdown:
    def __init__(self, refs):
        self._markdown = _Markdown(extensions=[
            AnchorExtension(refs),
            NdashExtension(),
            WrapperExtension(),
        ])

    def convert(self, content: str) -> str:
        return self._markdown.convert(content)
