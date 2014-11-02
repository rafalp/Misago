=============
Misago Markup
=============

Misago defines custom ``misago.markup`` module that provides facilities for parsing strings.

This module exposes following functions as its public API:


parse
-----

.. function:: parse(text, author=None, allow_mentions=True, allow_links=True, allow_images=True, allow_blocks=True)

Parses Misago-flavoured Markdown text according to settings provided. Returns dictionary with following keys:

* ``original_text``: original text that was parsed
* ``parsed_text``: parsed text
* ``markdown``: markdown instance


common_flavour
--------------

.. function:: common_flavour(text, author=None, allow_mentions=True)

Convenience function that wraps ``parse()``. This function is used for parsing messages.


Extending Markup
================

To extend Misago markup, create custom module defining one or both of following functions:


.. function:: extend_markdown(md)

Defining this function will allow you to register new extensions in markdown used to parse text.


.. function:: process_result(result, soup)

This function is called to allow additional changes in result dict as well as extra instrospection and cleanup of parsed text, which is provided as `Beautiful Soup <http://www.crummy.com/software/BeautifulSoup/bs4/doc/>`_ class instance.


Both functions should modify provided arguments in place.

Once your functions are done, add path to your module to ``MISAGO_MARKUP_EXTENSIONS`` setting which is tupe of modules.
