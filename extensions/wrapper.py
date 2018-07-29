from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from markdown.util import etree


class WrapperExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.treeprocessors.add('wrapper', ArticleWrapperTreeprocessor(md), '_begin')
        md.treeprocessors.add('extract_header', ExtractHeaderTreeprocessor(md), '>wrapper')


class ArticleWrapperTreeprocessor(Treeprocessor):
    def run(self, root):
        article = etree.Element('article')
        for attr, value in root.items():
            article.set(attr, value)
        for child in list(root):
            article.append(child)
        root.clear()
        root.append(article)


class ExtractHeaderTreeprocessor(Treeprocessor):
    def run(self, root):
        article = root.find('article')
        h1 = article.find('h1') if article is not None else None
        if h1 is not None:
            header = etree.Element('header')
            header.text = h1.text
            root.insert(0, header)
            article.remove(h1)
