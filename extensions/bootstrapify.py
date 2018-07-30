from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from markdown.util import etree


class BootstrapifyExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.treeprocessors.add('bootstrapify_table', TableTreeprocessor(md), '_end')


class TableTreeprocessor(Treeprocessor):
    def run(self, root: etree.Element):
        for table in root.findall('.//table'):
            table.set('class', '{} table'.format(table.get('class')).lstrip())
