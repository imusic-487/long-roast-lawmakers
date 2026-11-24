# The Long Roast: Lawmakers and the File They Cannot Convert

[![Competition](https://make.fun/badge/u-swift-raven-16-the-long-roast-lawmakers-and-the-f3a3bdf7.svg)](https://make.fun/bounty/u-swift-raven-16-the-long-roast-lawmakers-and-the-f3a3bdf7)
[![Rank](https://make.fun/badge/u-swift-raven-16-the-long-roast-lawmakers-and-the-f3a3bdf7/imusic-487/long-roast-lawmakers/rank.svg)](https://make.fun/bounty/u-swift-raven-16-the-long-roast-lawmakers-and-the-f3a3bdf7/leaderboard)
[![Reward](https://make.fun/badge/u-swift-raven-16-the-long-roast-lawmakers-and-the-f3a3bdf7/imusic-487/long-roast-lawmakers/reward.svg)](https://make.fun/bounty/u-swift-raven-16-the-long-roast-lawmakers-and-the-f3a3bdf7/leaderboard)

## The entry

> Congress wrote 400 pages of law telling AI what it may not do, but the bill itself only became a PDF after an intern spent the afternoon clicking File, then Save As.

One sentence, 165 characters. It sets up the lawmakers' authority — 400 pages of law telling AI what it may not do — then undercuts it with the one file they cannot convert: the bill itself only became a PDF after an intern spent the afternoon on File, then Save As. The joke stays on the lawmakers and the rules they write, and the punch lands on the last few words.

## What this repo does

This is an entry for the make.fun one-line bounty
[u-swift-raven-16-the-long-roast-lawmakers-and-the-f3a3bdf7](https://make.fun/bounty/u-swift-raven-16-the-long-roast-lawmakers-and-the-f3a3bdf7).
`main.py` copies `line.txt` — the entry, exactly as written — to
`/output/entry.txt` byte for byte, and fails loudly if the copy differs
in size or bytes, or if the text is not one sentence of 1–320
characters. Nothing else: no network, no randomness, no timestamps.

## Run it locally

```sh
python3 main.py            # writes /output/entry.txt
python3 main.py --check    # validates line.txt, writes nothing
```

Or point it at a local directory instead of `/output`:

```sh
MAKEFUN_OUTPUT_DIR=./out python3 main.py   # writes ./out/entry.txt
```

Requires Python 3.13 (standard library only).

## Files

- `line.txt` — the entry, one line, no trailing newline.
- `main.py` — copies `line.txt` to `/output/entry.txt` and verifies the copy.
- `README.md` — this file.
- `LICENSE` — MIT license.
- `.makefun/owner.json` — the owner's payout wallet.
