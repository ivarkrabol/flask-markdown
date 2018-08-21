from markdown import Markdown
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from markdown.util import etree


class FormatHrefsExtension(Extension):
    def extendMarkdown(self, md: Markdown, md_globals: dict) -> None:
        md.treeprocessors.add('strip_md', _FormatHrefsTreeprocessor(md), '_end')


class _FormatHrefsTreeprocessor(Treeprocessor):
    def run(self, root: etree.Element) -> None:
        for md_link in root.findall('.//a[@href]'):
            href = md_link.get('href')
            if href and href.endswith('/index.md'):
                md_link.set('href', href[:-8])
            elif href and href.endswith('.md'):
                md_link.set('href', href[:-3])
