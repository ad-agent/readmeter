# Usage guide

Run all examples from the project directory with Python 3.9 or newer.

## Read a text file

```bash
python3 readmeter.py examples/brief.txt
```

The output includes word, character, and line counts plus reading time.
For a path containing spaces, quote it: `python3 readmeter.py "my draft.txt"`.

## Read from a pipeline

```bash
printf 'Ship small. Document clearly.' | python3 readmeter.py -
```

The `-` argument reads UTF-8 data from standard input until the stream ends.

## Produce JSON

```bash
python3 readmeter.py examples/brief.txt --json
```

JSON fields are `source`, `words`, `characters`, `lines`, `reading_seconds`,
`reading_minutes`, and `words_per_minute`. With piped input, `source` is `stdin`.
An empty input produces zero counts and zero estimated reading time.

## Adjust reading speed

```bash
python3 readmeter.py README.md --wpm 150
```

Use a lower rate for dense material or a rate that fits your own pace.
The estimate does not account for images, equations, or time spent on examples.

## Counting conventions

- Characters include whitespace and newlines; these are Unicode code points.
- Lines follow Python's `splitlines()` behavior. A final newline does not add
  an extra empty line. File input normalizes CRLF to LF through Python's text reader.
- Apostrophes and hyphens inside words stay together: `don't` and `well-written`
  each count as one word. Punctuation by itself does not count as a word.
- Markdown, URLs, and code are counted as source text, not rendered content.
- The tool reads the complete input into memory; use it for drafts and documents.

## Troubleshooting

| Problem | Fix |
| --- | --- |
| `cannot read input` | Check the path, permissions, and UTF-8 encoding. |
| `--wpm must be greater than zero` | Supply a positive integer, such as `180`. |
| Unexpected Markdown count | Formatting and link destinations are included. |

The CLI exits with status `0` on success and `2` for invalid arguments or
unreadable input. Run `python3 readmeter.py --help` for all options.
