from markdown import Markdown
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from markdown.util import etree


class BootstrapifyExtension(Extension):
    def extendMarkdown(self, md: Markdown, md_globals: dict) -> None:
        md.treeprocessors.add('bootstrapify_table', _TableTreeprocessor(md), '_end')


class _TableTreeprocessor(Treeprocessor):
    def run(self, root: etree.Element) -> None:
        for table in root.findall('.//table'):
            table.set('class', '{} table'.format(table.get('class')).lstrip())
