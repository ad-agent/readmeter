"""Behavioral tests for word boundaries, estimates, and command-line errors."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from readmeter import analyze

CLI = Path(__file__).resolve().parents[1] / "readmeter.py"


class AnalysisTests(unittest.TestCase):
    def test_empty_document(self):
        result = analyze("")
        for key in ("words", "characters", "lines", "reading_seconds", "reading_minutes"):
            self.assertEqual(result[key], 0)

    def test_unicode_apostrophes_and_hyphens(self):
        self.assertEqual(analyze("Café déjà-vu isn't boring. It's well-written.")["words"], 6)
        self.assertEqual(analyze("It’s clear.")["words"], 2)

    def test_punctuation_is_not_a_word(self):
        self.assertEqual(analyze("... — !!! ___")["words"], 0)

    def test_minutes_round_up_at_boundary(self):
        self.assertEqual(analyze("word " * 200)["reading_minutes"], 1)
        self.assertEqual(analyze("word " * 201)["reading_minutes"], 2)
        self.assertEqual(analyze("word " * 201)["reading_seconds"], 61)

    def test_custom_speed(self):
        self.assertEqual(analyze("word " * 300, 150)["reading_seconds"], 120)

    def test_lines_and_characters(self):
        result = analyze("one\ntwo\n")
        self.assertEqual((result["lines"], result["characters"]), (2, 8))

    def test_invalid_speed(self):
        for speed in (0, -1):
            with self.assertRaises(ValueError):
                analyze("hello", speed)


class CommandLineTests(unittest.TestCase):
    def run_cli(self, *args, text=""):
        return subprocess.run(
            [sys.executable, str(CLI), *args],
            input=text.encode("utf-8"), capture_output=True,
        )

    def test_stdin_json(self):
        result = self.run_cli("-", "--json", text="Hello café!")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual((payload["source"], payload["words"]), ("stdin", 2))

    def test_file_input(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "sample.txt"
            source.write_text("A short document.", encoding="utf-8")
            result = self.run_cli(str(source), "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["words"], 3)

    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_cli(str(Path(directory) / "missing.txt"))
        self.assertEqual(result.returncode, 2)
        self.assertIn(b"cannot read input", result.stderr)

    def test_invalid_utf8(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "binary.txt"
            source.write_bytes(b"\xff\xfe")
            result = self.run_cli(str(source))
        self.assertEqual(result.returncode, 2)
        self.assertNotIn(b"Traceback", result.stderr)

    def test_zero_speed(self):
        result = self.run_cli("-", "--wpm", "0")
        self.assertEqual(result.returncode, 2)
        self.assertIn(b"greater than zero", result.stderr)


if __name__ == "__main__":
    unittest.main()
