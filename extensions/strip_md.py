from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from markdown.util import etree


class StripMdExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.treeprocessors.add('strip_md', StripMdTreeprocessor(md), '_end')


class StripMdTreeprocessor(Treeprocessor):
    def run(self, root: etree.Element):
        for md_link in root.findall('.//a[@href]'):
            href = md_link.get('href')
            if href and href.endswith('.md'):
                md_link.set('href', href[:-3])
