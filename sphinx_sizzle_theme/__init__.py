# -*- coding: utf-8 -*-
#
# Copyright 2019 by Vinay Sajip. All Rights Reserved.
#

from os import path
import xml.etree.ElementTree as ET

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

from docutils.nodes import strong, emphasis
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
    base_url = app.config['html_theme_options'].get('sitemap_url')
    if pagename != 'search' and base_url:
        url = urljoin(base_url, pagename + '.html')
        app.sitemap_urls.append(url)

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

    def visit_bullet_list(self, node):
        nda = node.non_default_attributes()
        if 'classes' in nda and 'detail-summary' in nda['classes']:
            hidden_detail = ['detail', 'hidden']
            summaries = []
            for li in node.children:
                summary = li.deepcopy()
                summary.attributes['classes'].append('summary')
                # lose all but the first children of the list item
                summary.children = summary.children[:1]
                para = summary.children[0]
                para.children = para.children[:1]
                handle = emphasis(classes=['fa', 'fa-arrow-circle-down'])
                handle.attributes['title'] = 'See more detail'
                para.insert(0, handle)
                li.attributes['classes'].extend(hidden_detail)
                handle = emphasis(classes=['fa', 'fa-arrow-circle-up'])
                handle.attributes['title'] = 'See less detail'
                li.children[0].insert(0, handle)
                summaries.append(summary)
            # now we have the summaries. Insert just before the detail items.
            n = len(node.children)
            for i in range(n - 1, -1, -1):
                node.insert(i, summaries[i])
        super(Translator, self).visit_bullet_list(node)

    def visit_emphasis(self, node):
        kwargs = {}
        if node.attributes:
            for k in ('title',):
                if k in node.attributes:
                    kwargs[k] = node.attributes[k]
        self.body.append(self.starttag(node, 'em', '', **kwargs))


def setup(app):
    app.add_html_theme('sizzle', path.abspath(path.dirname(__file__)))
    app.set_translator('html', Translator)
    app.connect('html-page-context', on_page)
    app.connect('build-finished', on_build_finished)
    app.add_role('fa', font_awesome)
    app.sitemap_urls = []
