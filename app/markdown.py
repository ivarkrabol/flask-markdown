from markdown import Markdown

from extensions import AnchorExtension, NdashExtension, WrapperExtension


md = Markdown(extensions=[
    AnchorExtension(),
    NdashExtension(),
    WrapperExtension(),
])


def markdown(content):
    return md.convert(content)
