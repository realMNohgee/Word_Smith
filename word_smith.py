#!/usr/bin/env python3
"""Word_Smith — text statistics and readability analysis from the command line.

Word_Smith analyzes text files for word count, character count, sentence count,
paragraph count, average word length, and readability scores (Flesch-Kincaid
Grade Level, Automated Readability Index).  Useful for writers, editors,
educators, and content pipelines.

Zero dependencies — pure Python stdlib.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter


# ── Text analysis ──────────────────────────────────────────────────────


def _count_words(text: str) -> int:
    """Count words (sequences of word characters)."""
    return len(re.findall(r"[^\W_]+", text, re.UNICODE))


def _count_sentences(text: str) -> int:
    """Count sentences by looking for terminal punctuation (., !, ?)."""
    # Split on sentence-ending punctuation followed by whitespace or end of string
    return len(re.findall(r"[.!?]+(?:\s+|$)", text))


def _count_paragraphs(text: str) -> int:
    """Count paragraphs (blocks of text separated by blank lines)."""
    # Split by double newlines
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    return len(paragraphs)


def _count_characters(text: str) -> int:
    """Count non-whitespace characters."""
    return len(re.sub(r"\s", "", text))


def _count_syllables(word: str) -> int:
    """Approximate syllable count for a single word."""
    word = word.lower().strip(".,!?;:\"'()[]{}")
    if not word:
        return 0
    # Count vowel groups
    count = len(re.findall(r"[aeiouy]+", word))
    # Adjust for silent e at end
    if word.endswith("e") and count > 0:
        count -= 1
    # Every word has at least one syllable
    return max(count, 1)


def _syllable_count(text: str) -> int:
    """Count total syllables across all words."""
    words = re.findall(r"[^\W_]+", text, re.UNICODE)
    return sum(_count_syllables(w) for w in words)


def analyze_text(text: str) -> dict:
    """Return a dict with all text statistics and readability scores."""
    words = _count_words(text)
    sentences = _count_sentences(text)
    paragraphs = _count_paragraphs(text)
    characters = _count_characters(text)
    syllables = _syllable_count(text)

    avg_word_len = characters / words if words > 0 else 0.0
    avg_sentence_len = words / sentences if sentences > 0 else 0.0

    # Flesch-Kincaid Grade Level
    if words > 0 and sentences > 0:
        fk_grade = 0.39 * avg_sentence_len + 11.8 * (syllables / words) - 15.59
    else:
        fk_grade = 0.0

    # Automated Readability Index (ARI)
    if words > 0 and sentences > 0:
        ari = 4.71 * (characters / words) + 0.5 * avg_sentence_len - 21.43
    else:
        ari = 0.0

    return {
        "word_count": words,
        "character_count": characters,
        "sentence_count": sentences,
        "paragraph_count": paragraphs,
        "syllable_count": syllables,
        "avg_word_length": round(avg_word_len, 2),
        "avg_sentence_length": round(avg_sentence_len, 2),
        "flesch_kincaid_grade": round(fk_grade, 1),
        "automated_readability_index": round(ari, 1),
    }


# ── Subcommand handlers ────────────────────────────────────────────────

def _read_input(args: argparse.Namespace) -> str:
    """Read text from a file or stdin."""
    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            print(f"Error: file not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        return sys.stdin.read()


def cmd_analyze(args: argparse.Namespace) -> int:
    """Full text analysis report."""
    try:
        text = _read_input(args)
    except SystemExit as e:
        return e.code if isinstance(e.code, int) else 1

    if not text.strip():
        print("Error: no text provided (empty input)", file=sys.stderr)
        return 1

    stats = analyze_text(text)

    if args.format == "json":
        print(json.dumps(stats, indent=2))
        return 0

    # Text report
    print("╔══════════════════════════════════════╗")
    print("║         Word_Smith  Analysis         ║")
    print("╚══════════════════════════════════════╝")
    print()
    print(f"  Word count:               {stats['word_count']:>8d}")
    print(f"  Character count:          {stats['character_count']:>8d}")
    print(f"  Sentence count:           {stats['sentence_count']:>8d}")
    print(f"  Paragraph count:          {stats['paragraph_count']:>8d}")
    print(f"  Syllable count:           {stats['syllable_count']:>8d}")
    print(f"  Avg. word length:         {stats['avg_word_length']:>8.1f}")
    print(f"  Avg. sentence length:     {stats['avg_sentence_length']:>8.1f}")
    print()
    print("  Readability Scores")
    print(f"  Flesch-Kincaid Grade:     {stats['flesch_kincaid_grade']:>8.1f}")
    print(f"  Automated Readability:    {stats['automated_readability_index']:>8.1f}")

    return 0


def cmd_count(args: argparse.Namespace) -> int:
    """Quick counts only (words, chars, sentences, paragraphs)."""
    try:
        text = _read_input(args)
    except SystemExit as e:
        return e.code if isinstance(e.code, int) else 1

    stats = analyze_text(text)
    result = {
        "word_count": stats["word_count"],
        "character_count": stats["character_count"],
        "sentence_count": stats["sentence_count"],
        "paragraph_count": stats["paragraph_count"],
    }
    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        print(f"Words: {result['word_count']}  "
              f"Chars: {result['character_count']}  "
              f"Sentences: {result['sentence_count']}  "
              f"Paragraphs: {result['paragraph_count']}")
    return 0


def cmd_grade(args: argparse.Namespace) -> int:
    """Readability grade level only."""
    try:
        text = _read_input(args)
    except SystemExit as e:
        return e.code if isinstance(e.code, int) else 1

    if not text.strip():
        print("Error: no text provided (empty input)", file=sys.stderr)
        return 1

    stats = analyze_text(text)
    result = {
        "flesch_kincaid_grade": stats["flesch_kincaid_grade"],
        "automated_readability_index": stats["automated_readability_index"],
    }
    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        print(f"Flesch-Kincaid Grade Level: {result['flesch_kincaid_grade']}")
        print(f"Automated Readability Index: {result['automated_readability_index']}")
    return 0


# ── Parser ─────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="word_smith",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--format", choices=["text", "json"], default="text",
                        help="Output format (default: text)")

    sub = p.add_subparsers(dest="cmd", required=True)

    s_analyze = sub.add_parser("analyze", parents=[common],
                               help="Full text analysis with readability scores")
    s_analyze.add_argument("file", nargs="?", help="Text file to analyze (reads stdin if omitted)")
    s_analyze.set_defaults(func=cmd_analyze)

    s_count = sub.add_parser("count", parents=[common],
                             help="Quick counts: words, chars, sentences, paragraphs")
    s_count.add_argument("file", nargs="?", help="Text file to count (reads stdin if omitted)")
    s_count.set_defaults(func=cmd_count)

    s_grade = sub.add_parser("grade", parents=[common],
                             help="Readability grade level only")
    s_grade.add_argument("file", nargs="?", help="Text file to grade (reads stdin if omitted)")
    s_grade.set_defaults(func=cmd_grade)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
