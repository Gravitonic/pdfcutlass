"""Command-line tool for editing PDF document outlines."""

import argparse
import json
import sys
from pypdf import PdfReader, PdfWriter


def load_parser():
    """Load the command-line argument parser."""

    parser = argparse.ArgumentParser(
        prog="pdfcutlass", description="Edit PDF outlines."
    )
    parser.add_argument("input_file")
    parser.add_argument("output_file")
    parser.add_argument("--outline")
    return parser


def main():
    """Main entry point for the application."""

    parser = load_parser()
    args = parser.parse_args()

    reader = PdfReader(args.input_file)

    writer = PdfWriter()
    writer.append(reader, import_outline=False)

    with open(args.outline, encoding="utf-8") as f:
        new_outline = json.load(f)

    current_parent = None

    for bookmark in new_outline:
        if "level" not in bookmark or bookmark["level"] == 1:
            current_parent = writer.add_outline_item(
                title=bookmark["title"],
                page_number=bookmark["page_number"] - 1,
            )
        elif current_parent is None:
            print("Error: no parent for child bookmark.", file=sys.stderr)
            sys.exit(1)
        else:
            writer.add_outline_item(
                title=bookmark["title"],
                page_number=bookmark["page_number"] - 1,
                parent=current_parent,
            )

    with open(args.output_file, "wb") as outfile:
        writer.write(outfile)


if __name__ == "__main__":
    main()
