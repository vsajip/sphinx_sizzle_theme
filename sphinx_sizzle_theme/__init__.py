# -*- coding: utf-8 -*-
#
# Copyright 2019-2022 by Vinay Sajip. All Rights Reserved.
#
from __future__ import print_function
import datetime
import inspect
import io
import json
import logging
from os import path, remove, close
import re
from shutil import rmtree
import sys
import tempfile
import xml.etree.ElementTree as ET

try:
    from urllib.parse import urljoin, urlencode
    from urllib.request import urlopen, Request
    basestring = str
except ImportError:
    from urlparse import urljoin
    from urllib import urlencode
    from urllib2 import urlopen, Request

from docutils.nodes import (strong, emphasis, inline, Text, document,
                            paragraph, reprunicode, raw)

from docutils.parsers.rst.roles import set_classes

# from sphinx import version_info as sphinx_version
from sphinx.addnodes import literal_strong
from sphinx.util.console import bold
from sphinx.writers.html import logger, HTMLTranslator as BaseTranslator

HERE = path.abspath(path.dirname(__file__))

__version__ = '0.1.1'

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

logging_enabled = False

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

_ICONIFY_PATTERN = re.compile(r'^(?P<icon_set>[\w-]+):(?P<icon>[\w-]+)(,(?P<height>\d+(\.\d+)?(px|r?em)))?(,(?P<classes>#?[\w-]+(,[\w-]+)*))?$')

_REMOVE_PATTERN = re.compile(r'xmlns(:xlink)?="[^"]+" ')

_ICON_DATA = {}

def iconify(role, rawText, text, lineno, inliner, options=None, context=None):
    if text in _ICON_DATA:
        svg = _ICON_DATA[text]
    else:
        m = _ICONIFY_PATTERN.match(text)
        if not m:
            raise ValueError('Invalid icon pattern: %r' % text)
        d = m.groupdict()
        url = 'https://api.iconify.design/%s/%s.svg' % (d['icon_set'], d['icon'])
        params = {}
        if d['height']:
            params['height'] = d['height']
        # import pdb; pdb.set_trace()
        if params:
            qs = urlencode(params)
            url = '%s?%s' % (url, qs)
        req = Request(url, headers={'User-Agent': 'sphinx-sizzle-theme'})
        resp = urlopen(req)
        # resp = requests.get(url, params=params)
        if resp.status != 200:
            s = '%s:%s' % (d['icon_set'], d['icon'])
            raise ValueError('Icon not found: %r' % s)
        s = resp.read().decode('utf-8')  # Might need to revisit
        if not d['classes']:
            attrs = ' class="iconify"'
        else:
            parts = d['classes'].split(',')
            attrs = ''
            if parts[0].startswith('#'):
                id = parts.pop(0)
                attrs = ' id="%s"' % id[1:]
            if 'iconify' not in parts:
                parts.append('iconify')
            attrs += ' class="%s"' % (' '.join(parts))
        svg = s.replace('<svg', '<svg%s' % attrs)
        svg = _REMOVE_PATTERN.sub('', svg)
        _ICON_DATA[text] = svg
    content = Text(svg)
    node = raw(format='html')
    node.append(content)
    # import pdb; pdb.set_trace()
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

_APP_JS_SNIPPET = '''
(function() {
  var sizzle = $(document).data('sizzle');

  sizzle.app_data = JSON.parse('%s');
})();
'''

def create_app_data(app):
    logger.info(bold('creating app data... '), nonl=True)
    filename = app.outdir + '/app-data.js'
    data = {
        'glossary': {
            'document': app.glossary_doc,
            'terms': app.glossary_info,
        },
        'custom_data': app.config.html_theme_options.get('custom_data', {})
    }
    s = json.dumps(data).replace('\\', '\\\\').replace('\'', '\\\'')
    s = _APP_JS_SNIPPET % s
    with io.open(filename, 'w', encoding='utf-8') as f:
        f.write(s)
    logger.info('done')

def on_init(app):
    app.first_permalinks = {}
    app.glossary_info = {}
    app.glossary_doc = None
    if logging_enabled:
        fd, fn = tempfile.mkstemp(prefix='sizzle-', suffix='.log')
        close(fd)
        fh = logging.FileHandler(fn, mode='w')
        logger.addHandler(fh)
        fh.setFormatter(logging.Formatter('%(levelname)-8s %(message)s'))
        logger.setLevel(logging.DEBUG)

    version = None
    try:
        fn = path.join(HERE, 'version.txt')
        if path.exists(fn):
            with io.open(fn, encoding='utf-8') as f:
                version = f.read().strip()
    except Exception:
        version = None
    app.sizzle_version = version

def on_build_finished(app, exception):
    if app.sitemap_urls:
        create_sitemap(app)
    create_app_data(app)

    # remove unused files.
    outdir = app.builder.outdir
    unused = (
        ('_static', 'jquery.js'),
        ('_static', 'jquery-3.2.1.js'),
        ('_static', 'underscore.js'),
        ('_static', 'underscore-1.3.1.js'),
        ('_static', 'ajax-loader.gif'),
        ('_static', 'comment.png'),
        ('_static', 'comment-bright.png'),
        ('_static', 'comment-close.png'),
        #('_static', 'file.png'),
        ('_static', 'up.png'),
        ('_static', 'up-pressed.png'),
        ('_static', 'down.png'),
        ('_static', 'down-pressed.png'),
        #('_static', 'plus.png'),
        #('_static', 'minus.png'),
        ('_static', 'basic.css'),
    )
    for cp in unused:
        p = path.join(outdir, *cp)
        if path.isfile(p):
            remove(p)
        elif path.isdir(p):
            rmtree(p)
    logger.debug('Build finished.')

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
    context['sizzle_version'] = app.sizzle_version
    context['build_date'] = datetime.date.today().strftime('%Y-%m-%d')
    if pagename != 'search':
        app_data_path = context['pathto']('search').replace('search.html',
                                                            'app-data.js')
        if app_data_path != '#':
            context['app_data_path'] = app_data_path
    logger.debug('on_page: %s', pagename)

def find_first_permalink(document):
    result = None
    for child in document.children:
        if child.tagname == 'section':
            ids = child.get('ids', [])
            if ids:
                result = ids[0]
                break
    return result

def find_docname():
    # Walk the stack until we find a frame with 'docname' in the locals.
    result = None
    for s in inspect.stack():
        if 'docname' in s.frame.f_locals:
            result = s.frame.f_locals['docname']
            break
    return result

def on_doctree_read(app, doctree):
    # Ideally, the docname would also have been made available ... but it hasn't
    # been. So, we try and use hackery to find it :-(
    #
    # This is so that the first permalink information is available as early as
    # possible in the process. The build process reads all the docs, and then
    # goes through each document doing a doctree-resolve and write operation.
    # The documents early in the process won't have the permalink information
    # that the later ones do.
    #
    # OK - disabled the stack hack for now, but may have to reinstate later
    #
    use_stack_hack = False
    if use_stack_hack:
        docname = find_docname()
        if docname:
            app.first_permalinks[docname] = find_first_permalink(doctree)
        logger.debug('on_doctree_read: %s', docname)

def on_doctree_resolved(app, doctree, docname):
    if docname not in app.first_permalinks:
        app.first_permalinks[docname] = find_first_permalink(doctree)
    logger.debug('on_doctree_resolved: %s', docname)

def extract_keys(source, keys):
    result = {}
    if not isinstance(keys, (list, tuple)):
        keys = keys.split()
    for key in keys:
        if key in source:
            result[key] = source[key]
    return result

def dump_node(node, level=0, file=sys.stdout):  # used for debugging only
    print('%s%r' %('  ' * level, node), file=file)
    for child in node.children:
        dump_node(child, level + 1, file=file)

class Translator(BaseTranslator):
    def __init__(self, *args, **kwargs):
        super(Translator, self).__init__(*args, **kwargs)
        self.li_level = 0
        toctree = False
        # Depending on Sphinx version, the document can be in different
        # positions in the argument list! Honestly ... just in case it moves
        # again, we look in the whole arg list and stop when a document is
        # found.
        for arg in args:
            if isinstance(arg, document):
                toctree = arg.children[0].get('toctree', False)
                break
        self.toctree = toctree
        if toctree:
            logger.debug('translate toctree: %s', self.builder.current_docname)
        # Remove limit on field names (ensures parameters are in two columns)
        self.settings.field_name_limit = 0
        self.in_glossary = self.in_field_body = False
        ctx = self.builder.globalcontext
        self.enable_tooltips = ctx.get('theme_enable_tooltips') in (True, 'true')
        self.glossary_permalinks = ctx.get('theme_glossary_permalinks') in (True, 'true')
        self.debugging = False

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

    def visit_list_item(self, node):
        if self.in_field_body:
            self.fixup_parameter(node[0])
        super(Translator, self).visit_list_item(node)
        self.li_level += 1

    def depart_list_item(self, node):
        self.li_level -= 1
        super(Translator, self).depart_list_item(node)

    def visit_reference(self, node):

        def get_link(docname):
            result = None
            app = self.builder.app
            if hasattr(app, 'first_permalinks'):
                result = app.first_permalinks.get(docname)
            return result

        ru = node.get('refuri')
        local = False
        if not self.toctree and node.get('internal') and not node.get('refid'):
            an = node.get('anchorname')
            if ru == '#' or an and an == ru:
                local = True

        # Fix up a bare '#' fragment to be a more sensible value.
        fragment_fixup = ((ru == '#') or                       # local TOC node
                          ('current' in node.get('classes')))  # global TOC node
        if fragment_fixup:
            link = get_link(self.builder.current_docname)
            if link:
                node['refuri'] = '#%s' % link
        if local:
            node.attributes['classes'].append('lvl-%d' % self.li_level)
        if (self.toctree and ru is not None and '#' not in ru and
            ru.endswith('.html')):
            name = ru.rsplit('.', 1)[0]
            while name.startswith('../'):
                name = name[3:]
            link = get_link(name)
            if link:
                node['refuri'] = '%s#%s' % (ru, link)
                logger.debug('visit_reference: %s -> %s', ru, node['refuri'])
        super(Translator, self).visit_reference(node)

    def fixup_parameter(self, node):
        # is this a parameter declaration with an oddly-parsed structure such
        # that we have a literal_strong for the parameter name, an ndash
        # separator, and then a paragraph? That needs slight massaging so we
        # don't have a dangling ndash ...
        if (isinstance(node[0], literal_strong) and
            (node[1] == ' \u2013 ') and isinstance(node[2], paragraph)):
            para = node[2]
            del node[2]
            #remove the paras children and insert them in place of the para
            for n in reversed(para.children):
                node.children.insert(2, n)

    def visit_field_body(self, node):
        self.in_field_body = True
        if len(node):
            self.fixup_parameter(node[0])
        super(Translator, self).visit_field_body(node)

    def depart_field_body(self, node):
        super(Translator, self).depart_field_body(node)
        self.in_field_body = False

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

    # For issue #6. Too bad we have to do copy-paste-edit here :-(
    def visit_label(self, node):
        self.body.append(self.starttag(node, 'td', '%s[' % self.context.pop(),
                                       CLASS='footnote-label'))

    # For issue #6. Too bad we have to do copy-paste-edit here :-(
    def visit_footnote(self, node):
        self.body.append(self.starttag(node, 'table',
                                       CLASS='docutils footnote',
                                       frame="void", rules="none"))
        self.body.append('<colgroup><col class="footnote-label" /><col /></colgroup>\n'
                         '<tbody valign="top">\n'
                         '<tr>')
        self.footnote_backrefs(node)

    # Glossary processing

    def visit_glossary(self, node):
        self.in_glossary = True
        b = self.builder
        if b.app.glossary_doc is None:
            b.app.glossary_doc = b.current_docname
        super(Translator, self).visit_glossary(node)

    def depart_glossary(self, node):
        super(Translator, self).depart_glossary(node)
        self.in_glossary = False

    def visit_term(self, node):
        super(Translator, self).visit_term(node)
        if self.in_glossary and self.enable_tooltips:
            self.term_key = node.attributes['ids'][0]
            self.term_pos = len(self.body)

    def depart_term(self, node):
        if self.in_glossary and self.enable_tooltips:
            term_html = ''.join(self.body[self.term_pos:])
            app = self.builder.app
            app.glossary_info.setdefault(self.term_key, {})['term'] = term_html
        if self.in_glossary and self.glossary_permalinks:
            s = ('<a class="headerlink" href="#%s" '
                 'title="Permalink to this term">\xb6</a>' % self.term_key)
            self.body.append(s)
        super(Translator, self).depart_term(node)

    def visit_definition(self, node):
        super(Translator, self).visit_definition(node)
        if self.in_glossary and self.enable_tooltips:
            self.defn_pos = len(self.body)

    def depart_definition(self, node):
        if self.in_glossary and self.enable_tooltips:
            defn_html = ''.join(self.body[self.defn_pos:])
            app = self.builder.app
            app.glossary_info.setdefault(self.term_key, {})['defn'] = defn_html
        super(Translator, self).depart_definition(node)


def setup(app):
    app.add_html_theme('sizzle', path.abspath(path.dirname(__file__)))
    app.set_translator('html', Translator)
    app.connect('builder-inited', on_init)
    app.connect('html-page-context', on_page)
    app.connect('build-finished', on_build_finished)
    app.connect('doctree-read', on_doctree_read)
    app.connect('doctree-resolved', on_doctree_resolved)
    app.add_role('fa', font_awesome)
    app.add_role('icon', iconify)
    app.add_role('span', generic_span)
    app.sitemap_urls = []
