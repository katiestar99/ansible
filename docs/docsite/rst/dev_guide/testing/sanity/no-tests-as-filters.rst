:orphan:

no-tests-as-filters
===================

Using Assible provided Jinja2 tests as filters will be removed in Assible 2.9.

Prior to Assible 2.5, Jinja2 tests included within Assible were most often used as filters. The large difference in use is that filters are referenced as ``variable | filter_name`` while Jinja2 tests are referenced as ``variable is test_name``.

Jinja2 tests are used for comparisons, whereas filters are used for data manipulation, and have different applications in Jinja2. This change is to help differentiate the concepts for a better understanding of Jinja2, and where each can be appropriately used.

As of Assible 2.5 using an Assible provided Jinja2 test with filter syntax will display a deprecation error.
