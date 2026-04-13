# Product Extractor

## Overview

This script will find files that are listed in a manifest and copy them to a new folder. It is intended to help isolate data products that failed validation for further processing or correction.

## Requirements

Python 3.10+

## Usage

```
/path/to/product_extractor.py manifest destination
```

`manifest` contains a list of files to copy. These must be relative paths unless you specify a prefix

`destination` is the directory that will receive the files.

### Optional Parameters

* `--prefix PREFIX`: This string will be removed from the beginning of the path before being copied to destination. Any files in the manifest that don't start with the prefix will be skipped.
* `--include-different-extensions`: When specified, this will also copy files that are the same except for the extension. This can help pick up files that go along with a label, assuming they have matching names.
* `--dry-run`: When specified, Product Extractor won't actually copy the files, it will only show what it would have done.
