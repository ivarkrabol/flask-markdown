from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern
from markdown.util import etree


class AnchorExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add('anchor', AnchorPattern(md), '_end')
        md.inlinePatterns.add('namedref', NamedRefPattern(md), '_begin')
        md.inlinePatterns.add('ref', RefPattern(md), '>namedref')


class AnchorPattern(Pattern):
    def __init__(self, markdown_instance=None):
        super().__init__(r'\{/([a-z:.]+)\}', markdown_instance)

    def handleMatch(self, m):
        name = m.group(2)

        el = etree.Element('a')
        el.set('name', name)
        return el


class RefPattern(Pattern):
    def __init__(self, markdown_instance=None):
        super().__init__(r'\[/([a-z:.]+)\]', markdown_instance)

    def handleMatch(self, m):
        label = m.group(2)

        href = label  # TODO: find correct link href
        text = label  # TODO: find correct link text

        el = etree.Element('a')
        el.set('href', href)
        el.text = text
        return el


class NamedRefPattern(Pattern):
    def __init__(self, markdown_instance=None):
        super().__init__(r'\[([^\]]+?)\]\(/([a-z:.]+)\)', markdown_instance)

    def handleMatch(self, m):
        text = m.group(2)
        label = m.group(3)

        href = label  # TODO: find correct link href

        el = etree.Element('a')
        el.set('href', href)
        el.text = text
        return el
