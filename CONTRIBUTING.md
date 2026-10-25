# Contributing

Readmeter aims to stay small, understandable, and dependency-free.

1. Open an issue describing the problem or improvement.
2. Create a focused branch and make your change.
3. Add a behavioral test when changing parsing or output.
4. Run `python3 -m unittest discover -s tests -v`.
5. Open a pull request explaining the change and how you checked it.

Keep compatibility with Python 3.9+. Avoid network requests in the CLI,
and document changes to the JSON fields. Documentation improvements
and small, reproducible bug reports are welcome.
