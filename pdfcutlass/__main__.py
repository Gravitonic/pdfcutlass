"""Command-line tool for editing PDF document outlines."""

import argparse
import json
import sys
from pathlib import Path
from pypdf import PdfReader, PdfWriter, PageRange


def load_parser():
    """Load the command-line argument parser."""

    parser = argparse.ArgumentParser(
        prog="pdfcutlass", description="Edit PDF outlines."
    )
    parser.add_argument("input_file")
    parser.add_argument("output_file")
    parser.add_argument("--outline", required=True)
    parser.add_argument("--split", action="store_true")
    return parser


def main():
    """Main entry point for the application."""

    parser = load_parser()
    args = parser.parse_args()

    reader = PdfReader(args.input_file)

    writer = PdfWriter()

    with open(args.outline, encoding="utf-8") as f:
        new_outline = json.load(f)

    current_parent = None

    if args.split:
        Path.mkdir(Path(args.output_file), exist_ok=True)

    for i, bookmark in enumerate(new_outline):
        if "level" not in bookmark or bookmark["level"] == 1:
            current_parent = writer.add_outline_item(
                title=bookmark["title"],
                page_number=bookmark["page_number"] - 1,
            )

            if args.split:
                section_writer = PdfWriter()

                next_bookmark_page = next(
                    (
                        e["page_number"] - 1
                        for e in new_outline[(i + 1) :]  # noqa: E203
                        if "level" not in e or e["level"] == 1
                    ),
                    None,
                )

                if next_bookmark_page == bookmark["page_number"] - 1:
                    continue

                page_range = PageRange(
                    slice(
                        bookmark["page_number"] - 1,
                        next_bookmark_page,
                    )
                )

                section_writer.append(
                    reader,
                    pages=page_range,
                    import_outline=False,
                )

                with open(
                    Path(args.output_file) / f"{bookmark['title']}.pdf", "wb"
                ) as outfile:
                    section_writer.write(outfile)
        elif current_parent is None:
            print("Error: no parent for child bookmark.", file=sys.stderr)
            sys.exit(1)
        else:
            writer.add_outline_item(
                title=bookmark["title"],
                page_number=bookmark["page_number"] - 1,
                parent=current_parent,
            )

    if not args.split:
        writer.append(reader, import_outline=False)
        with open(args.output_file, "wb") as outfile:
            writer.write(outfile)


if __name__ == "__main__":
    main()
