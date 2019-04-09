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

from sphinx.util.console import bold
from sphinx.writers.html import logger, HTMLTranslator as BaseTranslator

__version__ = '0.0.4'

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
            pass
            # TODO generate special markup for this type of list
        super(Translator, self).visit_bullet_list(node)

def setup(app):
    app.add_html_theme('sizzle', path.abspath(path.dirname(__file__)))
    app.set_translator('html', Translator)
    app.connect('html-page-context', on_page)
    app.connect('build-finished', on_build_finished)
    app.sitemap_urls = []
