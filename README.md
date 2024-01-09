# pdfcutlass

A very simple tool for splitting PDF documents.

## Usage

```
$ pdfcutlass -h
usage: pdfcutlass [-h] --outline OUTLINE [--split] input_file output_file

Edit PDF outlines.

positional arguments:
  input_file
  output_file

options:
  -h, --help         show this help message and exit
  --outline OUTLINE
  --split
```

The output file should be a PDF file name or, if using the `--split` option, should be the name of a directory. The outline should be a path to a JSON file that provides an array of bookmarks. For instance:

```json
[
  {
    "title": "Bookmark 1",
    "page_number": 1
  },
  {
    "title": "Bookmark 2",
    "page_number": 5
  },
  {
    "title": "Bookmark 2a",
    "page_number": 5,
    "level": 2
  },
  {
    "title": "Bookmark 2b",
    "page_number": 8,
    "level": 2
  },
  {
    "title": "Bookmark 3",
    "page_number": 10
  }
]
```

If the `--split` flag is enabled, each section will be output as a separate file. Currently, this only works with top-level bookmarks.

Otherwise, an output file will be generated with any previously existing bookmarks removed, and with the new outline specified in the outline file.
