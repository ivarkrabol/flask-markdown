from markdown import Markdown
from markdown.serializers import _write_html, ElementTree

from extensions.anchor import AnchorExtension
from extensions.ndash import NdashExtension


# class MyMarkdown(Markdown):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.serlializer = lambda element: _write_html(ElementTree(element).getroot(), format="xhtml")


md = Markdown(extensions=[AnchorExtension(), NdashExtension()])


def markdown(content):
    return md.convert(content)
