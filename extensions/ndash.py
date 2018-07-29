import re

from markdown.extensions import Extension
from markdown.postprocessors import Postprocessor

NDASH_PATTERN = re.compile(r'--')


class NdashExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.postprocessors.add('ndash', NdashPostprocessor(md), '_end')


class NdashPostprocessor(Postprocessor):
    def run(self, text):
        return NDASH_PATTERN.sub('&ndash;', text)
