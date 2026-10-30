#!/usr/bin/env python3
"""press_dom.py -- a small tolerant element tree for ThML / CCEL XML.

ThML files declare an external DTD and carry HTML entities and the odd
unbalanced tag, which xml.etree refuses. html.parser tolerates all of it; this
wraps it into a minimal tree (Node: tag, attrs, children; str for text).
Tag names come back lowercase (scripRef -> scripref).
"""
import html.parser

VOID = {"pb", "br", "img", "col", "hr", "insertindex", "meta", "link", "input", "added",
        "deleted", "index", "sync", "term"}

class Node:
    __slots__ = ("tag", "attrs", "children", "parent")
    def __init__(self, tag, attrs=None, parent=None):
        self.tag, self.attrs, self.children, self.parent = tag, dict(attrs or {}), [], parent
    def iter(self, tag=None):
        if tag is None or self.tag == tag:
            yield self
        for c in self.children:
            if isinstance(c, Node):
                yield from c.iter(tag)
    def find(self, tag):
        return next(self.iter(tag), None)
    def text(self):
        return "".join(c if isinstance(c, str) else c.text() for c in self.children)
    def __repr__(self):
        return f"<{self.tag} {self.attrs.get('id', '')}>"

class _Builder(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root")
        self.cur = self.root
    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.cur)
        self.cur.children.append(n)
        if tag not in VOID:
            self.cur = n
    def handle_startendtag(self, tag, attrs):
        self.cur.children.append(Node(tag, attrs, self.cur))
    def handle_endtag(self, tag):
        if tag in VOID:
            return
        n = self.cur
        while n is not self.root and n.tag != tag:
            n = n.parent
        if n is not self.root:          # close it (and anything left open inside)
            self.cur = n.parent
    def handle_data(self, data):
        self.cur.children.append(data)

def parse(text):
    b = _Builder()
    b.feed(text)
    b.close()
    return b.root
