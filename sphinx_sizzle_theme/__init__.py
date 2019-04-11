# -*- coding: utf-8 -*-
#
# Copyright 2019 by Vinay Sajip. All Rights Reserved.
#

from os import path
import xml.etree.ElementTree as ET

try:
    from urllib.parse import urljoin
    basestring = str
except ImportError:
    from urlparse import urljoin

from docutils.nodes import strong, emphasis, inline, Text
from docutils.parsers.rst.roles import set_classes

from sphinx.util.console import bold
from sphinx.writers.html import logger, HTMLTranslator as BaseTranslator

__version__ = '0.0.4'

def font_awesome(role, rawtext, text, lineno, inliner,
                 options=None, content=None):
    if options is None:
        options = {}
    classes = ['fa']
    options.update({'classes': classes})
    parts = text.split(',')
    classes.append('fa-%s' % parts.pop(0))
    classes.extend(parts)
    set_classes(options)
    node = emphasis(**options)
    return [node], []

def generic_span(role, rawText, text, lineno, inliner, options=None, context=None):
    if options is None:
        options = {}
    if '|' in text:
        ctext, text = text.split('|', 1)
        options['classes'] = ctext.split(',')
    content = Text(text)
    node = inline(**options)
    node.append(content)
    return [node], []

def create_sitemap(app):
    filename = app.outdir + '/sitemap.xml'
    logger.info(bold('creating sitemap... '), nonl=True)

    root = ET.Element('urlset')
    root.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')

    for link in app.sitemap_urls:
        url = ET.SubElement(root, 'url')
        ET.SubElement(url, 'loc').text = link

    ET.ElementTree(root).write(filename)
    logger.info('done')

def on_build_finished(app, exception):
    if app.sitemap_urls:
        create_sitemap(app)

def on_page(app, pagename, templatename, context, doctree):
    options = app.config['html_theme_options']
    base_url = options.get('sitemap_url')
    fonts = options.get('google_fonts')
    if pagename == 'index':
        if fonts:
            if isinstance(fonts, basestring):
                fonts = fonts.split(',')
            elif not isinstance(fonts, list):
                raise TypeError('The "fonts" theme option must be a string or '
                                'a list')
            context['theme_google_fonts'] = '|%s' % '|'.join(fonts)
    if pagename != 'search' and base_url:
        url = urljoin(base_url, pagename + '.html')
        app.sitemap_urls.append(url)

def extract_keys(source, keys):
    result = {}
    if not isinstance(keys, (list, tuple)):
        keys = keys.split()
    for key in keys:
        if key in source:
            result[key] = source[key]
    return result

class Translator(BaseTranslator):
    def visit_table(self, node, name=''):
        """
        Override docutils default table formatter to not include a border
        and to use Bootstrap CSS
        See: http://sourceforge.net/p/docutils/code/HEAD/tree/trunk/docutils/docutils/writers/html4css1/__init__.py#l1550
        """
        self.context.append(self.compact_p)
        self.compact_p = True
        # Let the user define whatever styles they want in the table ... we've
        # just overridden this method to prevent the border attribute being set!
        # classes = 'table table-bordered table-striped ' + self.settings.table_style
        # classes = classes.strip()
        # self.body.append(self.starttag(node, 'table', CLASS=classes))
        self.body.append(self.starttag(node, 'table'))

    def depart_table(self, node):
        self.compact_p = self.context.pop()
        self.body.append('</table>\n')

    def process_summary_detail_list(self, node):
        hidden_detail = ['detail', 'hidden']
        summaries = []
        for li in node.children:
            summary = li.deepcopy()
            summary.attributes['classes'].append('summary')
            # lose all but the first children of the list item
            summary.children = summary.children[:1]
            para = summary.children[0]
            para.children = para.children[:1]
            handle = inline(classes=['fa-li'])
            icon = emphasis(classes=['fa', 'fa-caret-right'])
            handle.append(icon)
            handle.attributes['title'] = 'See more detail'
            para.insert(0, handle)
            li.attributes['classes'].extend(hidden_detail)
            handle = inline(classes=['fa-li'])
            icon = emphasis(classes=['fa', 'fa-caret-down'])
            handle.append(icon)
            handle.attributes['title'] = 'See less detail'
            li.children[0].insert(0, handle)
            summaries.append(summary)
        # now we have the summaries. Insert just before the detail items.
        n = len(node.children)
        for i in range(n - 1, -1, -1):
            node.insert(i, summaries[i])

    def process_fa_styled(self, node, default_icon):
        def is_icon(node):
            if isinstance(node, Text):
                return False
            return 'fa' in node.attributes['classes']

        for li in node.children:
            para = li.children[0]
            icon = None
            if is_icon(para.children[0]):
                icon = para.pop(0)
            elif default_icon:
                icon = emphasis(classes=['fa', default_icon])
            handle = inline(classes=['fa-li'])
            if icon:
                handle.append(icon)
            para.insert(0, handle)

    def visit_bullet_list(self, node):
        nda = node.non_default_attributes()
        if 'classes' in nda:
            classes = nda['classes']
            if 'summary-detail' in classes:
                self.process_summary_detail_list(node)
                classes.append('fa-ul')
            elif 'styled-list' in classes:
                fa_class = None
                for c in classes:
                    if c.startswith('using-'):
                        fa_class = c
                        break
                if fa_class:
                    classes.remove(fa_class)
                    fa_class = fa_class.replace('using-', 'fa-')
                self.process_fa_styled(node, fa_class)
                classes.append('fa-ul')
        super(Translator, self).visit_bullet_list(node)

    def visit_emphasis(self, node):
        kwargs = {}
        if node.attributes:
            kwargs = extract_keys(node.attributes, 'title')
        if 'fa' in node.attributes['classes']:
            tagname = 'i'
        else:
            tagname = 'em'
        self.context.append(tagname)
        self.body.append(self.starttag(node, tagname, '', **kwargs))

    def depart_emphasis(self, node):
        tagname = self.context.pop()
        self.body.append('</%s>' % tagname)

    def visit_inline(self, node):
        kwargs = {}
        if node.attributes:
            kwargs = extract_keys(node.attributes, 'title')
        self.body.append(self.starttag(node, 'span', '', **kwargs))

def setup(app):
    app.add_html_theme('sizzle', path.abspath(path.dirname(__file__)))
    app.set_translator('html', Translator)
    app.connect('html-page-context', on_page)
    app.connect('build-finished', on_build_finished)
    app.add_role('fa', font_awesome)
    app.add_role('span', generic_span)
    app.sitemap_urls = []
