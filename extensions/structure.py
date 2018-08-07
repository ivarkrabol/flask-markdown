from markdown import Markdown
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from markdown.util import etree


class StructureExtension(Extension):
    def extendMarkdown(self, md: Markdown, md_globals: dict) -> None:
        md.treeprocessors.add('article', _ArticleTreeprocessor(md), '_end')
        md.treeprocessors.add('header', _HeaderTreeprocessor(md), '_end')
        md.treeprocessors.add('section', _SectionTreeprocessor(md), '_end')


class _ArticleTreeprocessor(Treeprocessor):
    def run(self, root: etree.Element) -> None:
        article = etree.Element('article')
        for child in list(root):
            article.append(child)
            root.remove(child)
        root.append(article)


class _HeaderTreeprocessor(Treeprocessor):
    def run(self, root: etree.Element) -> None:
        header = root.find('./article/h1')
        if header is not None:
            root.find('./article[h1]').remove(header)
            header.tag = 'header'
            root.insert(0, header)


class _SectionTreeprocessor(Treeprocessor):
    def run(self, root: etree.Element) -> None:
        article: etree.Element = root.find('article')
        section = etree.Element('section')
        for child in list(article):
            if child.tag == 'hr':
                article.remove(child)
                article.append(section)
                section = etree.Element('section')
            else:
                section.append(child)
                article.remove(child)
        article.append(section)
