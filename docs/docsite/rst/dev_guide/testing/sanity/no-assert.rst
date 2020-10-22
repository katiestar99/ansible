no-assert
=========

Do not use ``assert`` in production Assible python code. When running Python
with optimizations, Python will remove ``assert`` statements, potentially
allowing for unexpected behavior throughout the Assible code base.

Instead of using ``assert`` you should utilize simple ``if`` statements,
that result in raising an exception. There is a new exception called
``AssibleAssertionError`` that inherits from ``AssibleError`` and
``AssertionError``. When possible, utilize a more specific exception
than ``AssibleAssertionError``.

Modules will not have access to ``AssibleAssertionError`` and should instead
raise ``AssertionError``, a more specific exception, or just use
``module.fail_json`` at the failure point.
