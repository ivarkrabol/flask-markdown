from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern
from markdown.util import etree

from app.ref import Refs, ANCHOR_PATTERN_STR, RefNotFound


class AnchorExtension(Extension):
    def __init__(self, refs: Refs):
        super().__init__()
        self.refs = refs

    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add('ref', RefPattern(md, self.refs), '_begin')
        md.inlinePatterns.add('anchor', AnchorPattern(md), '>ref')


class RefPattern(Pattern):
    def __init__(self, markdown_instance, refs: Refs):
        super().__init__(r'\[([^\]]+?)\]\{([a-z:.]+)\}', markdown_instance)
        self.refs = refs

    def handleMatch(self, m):
        text = m.group(2)
        anchor = m.group(3)

        try:
            href = '/{}'.format(self.refs.find(anchor))
        except RefNotFound as err:
            print('RefNotFound: {}'.format(err))
            href = '/{}'.format(anchor)

        el = etree.Element('a')
        el.set('href', href)
        el.text = text
        return el


class AnchorPattern(Pattern):
    def __init__(self, markdown_instance):
        super().__init__(ANCHOR_PATTERN_STR, markdown_instance)

    def handleMatch(self, m):
        name = m.group(2)

        el = etree.Element('a')
        el.set('name', name)
        return el
