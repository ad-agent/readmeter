# Readmeter

**Know how long your next draft takes to read.**

![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-2563eb?style=flat-square)
![Dependencies: none](https://img.shields.io/badge/dependencies-none-16a34a?style=flat-square)
[![License: MIT](https://img.shields.io/badge/license-MIT-64748b?style=flat-square)](LICENSE)

A small, local-first CLI for word counts and reading-time estimates.
Built for writers, developers, and anyone shipping documentation.

## Why Readmeter?

- **Fast to start.** One Python file; no packages to install.
- **Useful metrics.** Words, characters, lines, and estimated reading time.
- **Script-friendly.** UTF-8 file input, standard input, and JSON output.
- **Private by design.** Text stays on your machine; the CLI makes no network calls.

## Quick start

Requires Python 3.9 or later. Run these commands from the project directory:

```bash
python3 readmeter.py examples/brief.txt
python3 readmeter.py README.md --json
printf 'A short and useful update.' | python3 readmeter.py - --wpm 180
```

## Options

| Option | Purpose | Default |
| --- | --- | --- |
| `file` | UTF-8 text file, or `-` for standard input | Required |
| `--wpm` | Reading speed; a positive integer | `200` |
| `--json` | Print structured JSON | Off |
| `--version` | Print the version | — |
| `--help` | Show command-line help | — |

## How the estimate works

Reading time is word count divided by words per minute, rounded up.
The default of 200 WPM is a configurable starting point, not a measured
reading speed. Empty text returns zero minutes.

Words are Unicode letter/number sequences, with internal apostrophes and
hyphens kept together. Markdown is counted as raw text, including links
and code. Languages without spaces may be undercounted. This is an
estimate for drafts, not a linguistic tokenizer or rendered-page parser.

## Development

```bash
python3 -m unittest discover -s tests -v
```

Tests cover word boundaries, reading-time rounding, UTF-8 input, JSON,
invalid speeds, and file errors. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE) · Created by [ad-agent](https://github.com/ad-agent).
