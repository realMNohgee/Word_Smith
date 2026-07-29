# Word_Smith 📝

**Analyze text readability, word counts, and grade levels from the terminal.** Zero dependencies, pure Python stdlib.

> Part of the Content & Education suite — gives writers, editors, and AI agents instant text analytics.

## One tool, many domains

| Domain | What Word_Smith does for you |
|---|---|
| ✍️ **Writing & Editing** | Check readability, sentence length, and grade level of drafts |
| 📚 **Education** | Assess whether texts are appropriate for target grade levels |
| 🤖 **AI Pipelines** | Add readability scoring to content-generation and filtering workflows |
| 📊 **Content Analytics** | Batch-analyze text corpora for linguistic statistics |
| 🧪 **Quality Assurance** | Gate content on minimum/maximum readability thresholds in CI |

## Install

```bash
git clone git@github.com:realMNohgee/Word_Smith.git
cd Word_Smith
python3 word_smith.py --help
```

## Quick start

```bash
# Full analysis report
python3 word_smith.py analyze myfile.txt

# Quick counts only
python3 word_smith.py count myfile.txt

# Just the readability grade
python3 word_smith.py grade myfile.txt

# Pipe from stdin
cat essay.txt | python3 word_smith.py analyze

# JSON output for pipelines
python3 word_smith.py analyze report.txt --format json
```

## Metrics

| Metric | Description |
|---|---|
| Word count | Total non-symbol words |
| Character count | Non-whitespace characters |
| Sentence count | Sentences detected via `.`, `!`, `?` |
| Paragraph count | Blocks separated by blank lines |
| Average word length | Characters per word |
| Average sentence length | Words per sentence |
| Flesch-Kincaid Grade | US grade-level readability score |
| Automated Readability Index | Alternative grade-level formula |

## Subcommands

- **`analyze`** — Full text analysis with all statistics and readability scores
- **`count`** — Quick counts: words, characters, sentences, paragraphs
- **`grade`** — Readability grade level only (Flesch-Kincaid + ARI)

All subcommands accept an optional file argument (reads stdin if omitted) and support `--format text|json`.

## License

MIT — see [LICENSE](LICENSE).

---

🧰 **[Tool on Hermtica Marketplace](https://hermtica.com/marketplace)** — the open, agent-agnostic marketplace for AI agent tools.
