"""The Long Roast: Lawmakers and the File They Cannot Convert.

Copies line.txt (the entry: one satirical sentence, 1-320 characters)
to /output/entry.txt byte for byte. MAKEFUN_OUTPUT_DIR, when set,
stands in for /output so the entry can be tested locally.

Usage:
    python3 main.py                        # write /output/entry.txt
    python3 main.py --check                # validate line.txt only, write nothing
    python3 main.py --output-dir ./out    # write ./out/entry.txt instead

Fails loudly if anything is off: line.txt is missing, it is not valid
UTF-8, it is not 1-320 characters, it is only white space, it has
leading or trailing white space, it contains a line break or a control
character, or the written copy differs from line.txt in size or bytes.
Every failure reports the actual value against the expected value, so
a bad entry cannot pass silently.

Standard library only. No network, no randomness, no timestamps.
"""

import argparse
import hashlib
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LINE_FILE = HERE / "line.txt"
DEFAULT_OUTPUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
MIN_CHARS = 1
MAX_CHARS = 320


def resolve_output_dir(args):
    """Pick the output directory: --output-dir wins over the env var."""
    if args.output_dir is not None:
        return Path(args.output_dir)
    return DEFAULT_OUTPUT_DIR


def fail(message):
    """Report a failure the way the gate would see it, then stop."""
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_entry():
    """Read line.txt as raw bytes, then decode it as strict UTF-8."""
    try:
        raw = LINE_FILE.read_bytes()
    except FileNotFoundError:
        raise RuntimeError(f"missing entry source: expected {LINE_FILE}")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        fail(f"entry is not valid UTF-8: {exc} (expected UTF-8 text)")
    return raw, text


def check_entry(text):
    """Check the entry against the gate, reporting actual vs expected."""
    size = len(text)
    if size < MIN_CHARS or size > MAX_CHARS:
        fail(f"entry is {size} characters, expected {MIN_CHARS}-{MAX_CHARS}")
    if text.strip() == "":
        fail("entry is only white space, expected visible text")
    if text != text.strip():
        fail(
            "entry has leading or trailing white space: "
            f"stripped length is {len(text.strip())}, raw length is {size}"
        )
    if "\n" in text or "\r" in text:
        fail("entry must be a single line, no line breaks")
    for position, char in enumerate(text):
        code = ord(char)
        if code < 0x20 or code == 0x7F:
            fail(
                "entry contains a control character at position "
                f"{position}: U+{code:04X}"
            )
    terminators = ".!?"
    stops = sum(1 for char in text if char in terminators)
    if stops != 1 or text[-1] not in terminators:
        fail(
            "entry must be exactly one sentence ending with a full stop, "
            f"found {stops} sentence terminators"
        )


def write_entry(raw, text, output_dir):
    """Write the entry byte for byte, then read it back and verify.

    The write goes to a temporary file first and is then moved into
    place, so a failed run can never leave a half-written entry.txt
    behind for the gate to read.
    """
    output_file = output_dir / "entry.txt"
    output_dir.mkdir(parents=True, exist_ok=True)
    temp_file = output_dir / "entry.txt.tmp"
    temp_file.write_bytes(raw)
    os.replace(temp_file, output_file)
    written = output_file.read_bytes()
    if written != raw:
        fail(
            "written copy differs from line.txt: "
            f"wrote {len(written)} bytes, expected {len(raw)} bytes"
        )
    digest = hashlib.sha256(written).hexdigest()
    print(
        f"entry ok: {len(written)} bytes, {len(text)} characters, "
        f"sha256 {digest}"
    )


def parse_args(argv):
    """Parse the flags this program takes: --check and --output-dir."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate line.txt only, write nothing",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="write entry.txt here instead of $MAKEFUN_OUTPUT_DIR or /output",
    )
    return parser.parse_args(argv)


def main(argv=None):
    """Load the entry, check it, and either report or write it out."""
    args = parse_args(argv)
    raw, text = load_entry()
    check_entry(text)
    if args.check:
        digest = hashlib.sha256(raw).hexdigest()
        print(
            f"entry ok: {len(raw)} bytes, {len(text)} characters, "
            f"sha256 {digest} (checked, nothing written)"
        )
        return 0
    write_entry(raw, text, resolve_output_dir(args))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
