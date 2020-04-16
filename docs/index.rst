.. Sizzle documentation master file, created by
   sphinx-quickstart on Fri Apr 12 07:44:40 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

The Sizzle theme for Sphinx
===========================

This documentation describes Sizzle, a theme for Sphinx_. This theme was
inspired by another theme, Guzzle_. Sizzle uses some of the styling elements of
Guzzle, but has diverged a fair bit in numerous areas.

.. _Sphinx: https://www.sphinx-doc.org/

.. _Guzzle: https://github.com/guzzle/guzzle_sphinx_theme

The repository where this theme is developed is to be found `here
<https://bitbucket.org/vinay.sajip/sphinx_sizzle_theme/>`_.


Theme Options
~~~~~~~~~~~~~

Sizzle inherits from Sphinx's ``basic`` theme. The following theme options are defined:

* ``globaltoc_collapse`` -- as for Guzzle: this determines whether the global TOC
  shown in the sidebar is collapsed or not. Defaults to ``false``.
* ``globaltoc_depth`` -- as for Guzzle: the depth to which the global TOC is
  expanded. Defaults to ``5``.
* ``globaltoc_includehidden`` -- as for Guzzle: whether to include hidden entries
  in the global TOC. Defaults to ``true``.
* ``project_logo_name`` -- this replaces Guzzle's ``project_nav_name``. The name
  change reflects that the value can be shown elsewhere than in a navigation
  panel.
* ``sitemap_url`` -- this replaces Guzzle's ``base_url``. The new name better
  reflects how the value is used - as a base URL for sitemap links.
* ``google_fonts`` -- this allows you to specify additional Google fonts to be
  included for use in any custom styles. Defaults to ``None``.
* ``google_analytics_id`` -- this replaces Guzzle's ``google_analytics_account``.
  The name better reflects that the value is a tracker ID.
* ``show_index`` -- controls whether a link to the index is shown in the header.
  This defaults to ``true`` - set it to ``False`` to hide the link.
* ``show_filter`` -- controls whether a filter to apply to TOC titles is shown.
  This defaults to ``true`` - set it to ``False`` to hide the filter (which is
  not needed if you have a short enough list of entries in the TOC).
* ``enable_tooltips`` -- controls if tooltips are shown. This defaults to
  ``true`` - set it to ``False`` to disable tooltips.
* ``glossary_permalinks`` -- controls if glossary terms have permalinks. This
  defaults to ``true`` - set it to ``False`` to disable the permalinks.
* ``custom_data`` -- any custom data used by the theme. This defaults to an empty
  dictionary. This data needs to be loaded by JavaScript code in the HTML
  documentation, and so it should only contain content which is amenable to being
  serialized using JSON.

.. versionadded:: 0.0.9 The ``custom_data`` theme element was added.

Layout
~~~~~~

The layout has a scrolling area, consisting of sidebar and content, between a
fixed header and footer. The footer is small (for copyright information and
links) and the header has the following elements:

* A gradient background
* The project name (as determined by ``project_logo_name``). Except when in the
  home page, you can click on this to get to the home page
* The title of the current document
* The search box, assuming the browser window is wide enough. If it isn't, the
  search box relocates to the top of the sidebar.
* A link to the index. This is conditionally visible (controlled by
  the ``show_index`` theme option) and styled as a button
* A link to the source for the current page, if available. This is conditionally
  visible (controlled by the ``show_source`` option) and styled as a button
* Links (styled as buttons) to take you to previous and next pages, if any

The sidebar and content area can scroll independently.

Sidebar
+++++++

The sidebar contains the following, from top to bottom:

* If the browser window isn't wide enough to accommodate it, the
  search box.
* The heading "Table of Contents", alongside which there is a left chevron
  ( :fa:`chevron-left` ) which can be clicked on to collapse the sidebar.
* A "Filter by title" input box. If there is a long list of TOC entries, this
  is handy to be able to filter the TOC entries by title. If you type into it,
  only TOC entries with titles matching the filter text will be shown. The
  ``show_filter`` theme option can be used to control the visibility of the
  box.

If the sidebar is collapsed, you can bring it back by hovering the mouse at the
left edge of the browser window for a second or two.

You can also hide and show the sidebar via the keyboard:

* Press :kbd:`Control-left arrow` to hide it.
* Press :kbd:`Control-right arrow` to show it.

Typography
~~~~~~~~~~

* `Font Awesome <https://fontawesome.com/v4.7.0/>`_ is integrated. You can use
  the markup role ``fa`` to introduce an icon into your content. For example,
  the markup ``:fa:`diamond``` produces :fa:`diamond` in the finished output.
* Document and section titles use `Source Serif Pro
  <https://en.wikipedia.org/wiki/Source_Serif_Pro>`_.
* The default body font is `Roboto <https://en.wikipedia.org/wiki/Roboto>`_,
  falling back to Guzzle's slightly less compact choice of
  `Open Sans <https://en.wikipedia.org/wiki/Open_Sans>`_.
* The monospace font used for code blocks is `Iosevka
  <https://en.wikipedia.org/wiki/Iosevka>`_, which is a condensed font allowing
  more content to be shown than the fallbacks of `Roboto Mono
  <https://en.wikipedia.org/wiki/Roboto#Roboto_Mono>`_,
  `Source Code Pro <https://en.wikipedia.org/wiki/Source_Code_Pro>`_ and
  `Consolas <https://en.wikipedia.org/wiki/Consolas>`_. An example:

  .. code::

    @real fox.quick(h) { *is_brown && it_jumps_over(doges.lazy) }

Google Fonts
~~~~~~~~~~~~

If you want to use other Google fonts in your documentation, you can do this
via a theme option::

    html_theme_options = {
        # other stuff omitted
        'google_fonts': ['Acme', 'Raleway:400,700'],
        # other stuff omitted
    }

This would make the ``Acme`` and ``Raleway`` fonts (the latter with the
specific weights indicated) for use in your documentation, so that you could
use ``Acme`` and ``Raleway`` in ``font-family`` values in your custom CSS.

Custom Roles
~~~~~~~~~~~~

This theme adds two specific roles which you might find useful in documenting
your projects:

* The ``fa`` role, as described above.
* A generic ``span`` role, which can be used as follows: the markup
  ``:span:`c1,c2,c3|some text``` will result in the output

  .. code-block:: html

     <span class="c1 c2 c3">some text</span>

  This isn't intended to be used to provide lots of ad-hoc styles (which would
  detract from the quality of the documentation), but it can be useful in some
  scenarios (such as trying things out). You can, of course, create your own
  roles in reStructuredText markup using the `role directive
  <http://docutils.sourceforge.net/docs/ref/rst/directives.html#role>`_

  ``.. role:: <rolename>``

  This approach is preferable when your usage of a particular style is
  systematic rather than *ad hoc*.

  The sections on :ref:`summary_detail` and :ref:`custom_tooltips` give examples where
  the ``span`` role can be useful.

Use of JavaScript, CSS and font assets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The version of jQuery used is 3.3.1. The version of Bootstrap used is 3.3.7.
These are loaded from CDN, as are the fonts. No additional external assets
beyond these are used, though you can add some in the usual way to a specific
project -- see the section :ref:`custom` for more details.

Styling Lists using Font Awesome
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can style bulleted lists using Font Awesome. For example, the following
list:

.. cssclass:: styled-list using-star

* Arcturus
* Betelgeuse
* VY Canis Majoris

was produced using this markup:

.. code-block:: rst

    .. cssclass:: styled-list using-star

    * Arcturus
    * Betelgeuse
    * VY Canis Majoris

A class starting with ``using-`` is used to style the list, with ``using-`` being
replaced by ``fa-`` in the actual style applied.

You can override individual items with specific icons. For example,

.. cssclass:: styled-list using-star

* :fa:`star-o` Arcturus
* :fa:`star-half-o` Betelgeuse
* VY Canis Majoris

was produced by this markup:

.. code-block:: rst

    .. cssclass:: styled-list using-star

    * :fa:`star-o` Arcturus
    * :fa:`star-half-o` Betelgeuse
    * VY Canis Majoris

.. _summary_detail:

Summary-Detail Lists
~~~~~~~~~~~~~~~~~~~~

HTML5 has a handy feature - summary-detail lists, which are marked up like this:

.. code-block:: html

    <details>
      <summary>The summary goes here.</summary>
      <p>The detail goes here.</p>
    </details>

The idea is that the whole thing can be closed (when only the summary is
visible) or open (when both the summary and detail parts are visible). However,
browser support is patchy and inconsistent, and styling options are limited.

Here's how the element looks when open and closed in Firefox and Chrome:

.. cssclass:: table table-bordered

===================================== =================================== ========================================= ======================================
Closed (Firefox)                      Open (Firefox)                      Closed (Chrome)                           Open (Chrome)
===================================== =================================== ========================================= ======================================
.. image:: _static/img/ff-closed.png  .. image:: _static/img/ff-open.png  .. image:: _static/img/chrome-closed.png  .. image:: _static/img/chrome-open.png
===================================== =================================== ========================================= ======================================

Of course, docutils and Sphinx don't offer any reStructuredText markup which
maps to this HTML5 element. With the Sizzle theme, you can achieve a similar
effect like this:

.. code-block:: rst

    .. cssclass:: summary-detail

    * :span:`The summary goes here.`

      The detail goes here.

The Sizzle theme code looks for this specific CSS class and arranges for it to
be shown like this:

.. cssclass:: summary-detail

* :span:`The summary goes here.`

  The detail goes here.


.. _custom:

Custom Styles and JavaScript
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have custom styles and/or JavaScript, you can install them in one of
two ways, depending on the version of Sphinx you're using. If you're using
Sphinx 1.8 or later, you should use configuration options in :file:`conf.py`
like this:

.. code-block:: python

    html_css_files = ['css/project.css']
    html_js_files = ['js/project.js']

If you're using an earlier Sphinx version than 1.8, then in your
:file:`conf.py`, have code something like this:

.. code-block:: python

    def setup(app):
        app.add_stylesheet('css/project.css')
        app.add_javascript('js/project.js')

The CSS file will be loaded *after* Sizzle's own CSS, allowing you to tweak
styles where needed. The JavaScript file will be added after all other external
JavaScript files. Bear in mind that the Sizzle theme arranges to first add a
JavaScript object to the DOM using a jQuery call:

.. code-block:: javascript

    $(document).data('sizzle', {on_load: []});  // code in the Sizzle theme

This is done *before* your custom JavaScript is included. If you want to have
some JavaScript code of yours called after the entire document is loaded, you
can do something like

.. code-block:: javascript

    function my_custom_function() {
      // whatever
    }

    var sizzle = $(document).data('sizzle');

    sizzle.on_load.push(my_custom_function);

in your custom JavaScript file. When the document has loaded, the Sizzle
theme's code calls any functions pushed onto the ``on_load`` array:

.. code-block:: javascript

      $(document).ready(function() {  // code in the Sizzle theme

        // other stuff omitted ...

        var sizzle = $(document).data('sizzle');

        if (sizzle.on_load) {
          sizzle.on_load.forEach(function(f) {
            f();
          });
        }

        // other stuff omitted ...

      }

So your ``my_custom_function`` should get called once the document has loaded.

.. _style-cols:

Example -- styling columns in a table
+++++++++++++++++++++++++++++++++++++

Here's an example function which I implemented for a project, using the
functionality described above:

.. code-block:: javascript

    function add_column_styles() {
      $('table').each(function() {
        $(this).find('tr').each(function() {
          $(this).find('td, th').each(function(i) {
            $(this).addClass('col-' + i);
          });
        });
      });
    }

This adds a ``col-N`` class to every cell in the Nth column of every table,
including header rows. By judicious application of CSS, you might be able to
use this approach to style tables in your content as you wish. For instance,

.. code-block:: css

    /* centre all columns except the first */
    #some-table td:not(.col-0), #some-table th:not(.col-0) {
      text-align: center;
    }

    /* apply padding to the first column only */
    #some-table td.col-0, #some-table th.col-0 {
      padding-left: 6px;
    }


Device-Friendliness
~~~~~~~~~~~~~~~~~~~

The theme adapts well to smaller screens, as shown in the following images.

.. cssclass:: table table-bordered

==================================== ===================================
Appearance on a small screen         Navigation menu on a small screen
==================================== ===================================
.. image:: _static/img/mobile_1.png  .. image:: _static/img/mobile_2.png
==================================== ===================================

Navigation Improvements
~~~~~~~~~~~~~~~~~~~~~~~

In larger documentation sets, the list of items in the navigator is quite long -
if you use it to navigate to a different page, then the navigator would normally
be positioned at the top, rather than in the vicinity of the element you clicked
to get to that page. The Sizzle theme JavaScript code tries to position the link
which led you to a particular part of the documentation to near the vertical
centre of the navigator, or at least in the visible portion of the navigator.

Glossary Improvements
~~~~~~~~~~~~~~~~~~~~~

Starting with version 0.0.9, there have been some improvements to Sphinx
glossary functionality.

Tooltips
++++++++

By default, you can see tooltips when you hover over a glossary term in
documentation. You can try them out in the `Supervisor documentation set
<https://docs.red-dove.com/supervisor/>`_: there are some glossary terms at
the top of the home page - just hover over them to see the tooltips with the
glossary definitions of those terms.

You can disable tooltips by setting ``enable_tooltips`` to ``False`` in the
theme options.

.. versionadded:: 0.0.9
   The tooltip functionality was added and applied to glossary terms.

Permalinks
++++++++++

In the glossary, the term headings have a hover-over permalink which allows
you to bookmark them by right-clicking -- the same as headings.

You can disable glossary permalinks by setting ``glossary_permalinks`` to
``False`` in the theme options.

Code Block Improvements
~~~~~~~~~~~~~~~~~~~~~~~

Starting with version 0.0.9, code blocks with captions get a little button
which, when clicked, copies the contents of the code block to the clipboard.
The idea was shamelessly borrowed from recent Django documentation! Here's an
example:

.. code-block:: python3
   :caption: dump_node.py

   def dump_node(node, level=0, file=sys.stdout):  # used for debugging only
       print('%s%r' %('  ' * level, node), file=file)
       for child in node.children:
           dump_node(child, level + 1, file=file)

.. versionadded:: 0.0.9
   The code block copy functionality was added.

.. _custom_tooltips:

Providing Customized Tooltips
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Starting with version 0.0.9, you can provide customized tooltips. For example, here's
an info icon with a customized tooltip: :fa:`info-circle,tc-infotip,tci-ver-0.0.9`
:span:`tc-info|` If you hover over it, you'll see a tooltip saying something like
"This feature was added in version 0.0.9." This was achieved using the following
steps:

* Have a span with a CSS class ``tc-infotip`` and another CSS class starting with ``tci-``,
  where the suffix is treated as a key. to use when finding the tooltip's HTML. In the
  above example, that's done using the markup
  ``:fa:`info-circle,tc-infotip,tci-ver-0.0.9```. The ``tc-infotip`` class is used to
  style the content with the tip (by default, it just indicates via the cursor that
  help is available).
* Immediately following that, have a span which has the ``tc-info`` class. IN the above
  example, that's just ```:span:`tc-info|``` (the span here has no text; it simply
  serves as a marker for the preceding element. But it's fine to have text, too, as in
  the examples below).
* In :file:`conf.py`, the ``custom_data`` theme option was set to have some pertinent
  information, like this:

  .. code-block:: python

      'custom_data': {
        'info-tips': {
            'ver-0.0.9': 'This feature was added in version 0.0.9.',
            'win-only': 'This doodad only works on Windows.',
            'linux-only': 'This thingummy is for Linux only.',
        },
    }

When the documentation is built, Python code in the Sizzle theme ensures that the
contents of ``custom_data`` are made available to the JavaScript code in the built
documentation. When the page is loaded, JavaScript code in the Sizzle theme looks for
elements with class ``tc-info`` and for each of them, if an element is found
immediately preceding it with a class beginning with ``tci-``, that prefix is stripped
off to provide a key (in this case, it would be ``ver-0.0.9``. If that key is found in
the ``info-tips`` mapping, the corresponding value is treated as HTML to appear in the
tooltip. (If the key is not found, e.g. because missing or misspelt in
``custom_data['info-tips']``, then no tooltip will appear.)

Of course, Sphinx has ``versionadded`` and ``versionchanged`` directives to provide
this type of information in the body of the document. But this example is just for the
purposes of illustration -- in practice, this feature could be used to provide
info-tips which are about platform-specific or product-specific features, with a
suitable icon to draw attention to them. For example, to mark something as only
working on :fa:`windows,tc-infotip,tci-win-only` :span:`tc-info|Windows`, or something else as
only working on :fa:`linux,tc-infotip,tci-linux-only` :span:`tc-info|Linux`.

.. versionadded:: 0.0.9
   Customized tooltip functionality was added.

Change Log
~~~~~~~~~~



.. cssclass:: summary-detail

    * :span:`Changes for recent releases are shown here (click the arrow at left to
      expand).`

      .. cssclass:: table table-striped

      +------------+------------+----------------------------------------------------+
      |Version     |Released on |Changes                                             |
      +============+============+====================================================+
      |0.0.9       |17 Apr 2020 |Add glossary improvements (allowing permalinks to   |
      |            |            |terms, providing tooltips for term definitions).    |
      |            |            |                                                    |
      |            |            |Allow code blocks with captions to be copied with a |
      |            |            |click.                                              |
      |            |            |                                                    |
      |            |            |Provide a means of showing customized tooltips.     |
      +------------+------------+----------------------------------------------------+
      |0.0.8       |16 Oct 2019 |Improved documentation.                             |
      |            |            |                                                    |
      |            |            |Fixed some minor styling nits (e.g. equation        |
      |            |            |colors).                                            |
      |            |            |                                                    |
      |            |            |Added the 'linktags' block to the layout.           |
      |            |            |                                                    |
      |            |            |Allowed keyboard navigation without having to click |
      |            |            |on the page first.                                  |
      +------------+------------+----------------------------------------------------+
      |0.0.7       |10 May 2019 |Improved tarball generation.                        |
      |            |            |                                                    |
      |            |            |Updated documentation, layout, styles and logic.    |
      +------------+------------+----------------------------------------------------+
      |0.0.6       |07 May 2019 |Removed unused files when building documentation.   |
      |            |            |                                                    |
      |            |            |Improved navigation logic further.                  |
      +------------+------------+----------------------------------------------------+
      |0.0.5       |18 Apr 2019 |Updated styles and layout.                          |
      |            |            |                                                    |
      |            |            |Improved navigation logic.                          |
      +------------+------------+----------------------------------------------------+
      |0.0.4       |12 Apr 2019 |Updated README.                                     |
      |            |            |                                                    |
      |            |            |Added documentation and prepared to dogfood theme.  |
      |            |            |                                                    |
      |            |            |Made changes to styles, layout and JavaScript code. |
      |            |            |                                                    |
      |            |            |Announced on sphinx-users, feedback solicited.      |
      +------------+------------+----------------------------------------------------+
      |0.0.3       |09 Apr 2019 |Made style, layout and JavaScript changes.          |
      |            |            |                                                    |
      |            |            |Added LICENSE file.                                 |
      |            |            |                                                    |
      |            |            |Switched to SCSS for style source.                  |
      +------------+------------+----------------------------------------------------+
      |0.0.2       |07 Apr 2019 |Updated README.                                     |
      +------------+------------+----------------------------------------------------+
      |0.0.1       |07 Apr 2019 |Initial release.                                    |
      +------------+------------+----------------------------------------------------+
