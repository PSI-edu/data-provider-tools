#! /usr/bin/env python3
"""
Copy all of the specified files to a new directory, preserving the directory structure.
"""

import argparse
import os
import shutil
import glob
import logging
import sys


def main():
    parser = argparse.ArgumentParser(
        description="Copy all of the specified files to a new directory, preserving the directory structure."
    )
    parser.add_argument(
        "--prefix",
        type=str,
        help="The path prefix to remove from the files. Files that do not start with this prefix will be skipped.",
    )
    parser.add_argument(
        "--include-different-extensions",
        action="store_true",
        help="Include files with the same base name but different extensions. If this option is not specified, only the files with the same extension as the manifest file will be included.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not copy the files, just print the operations",
    )
    parser.add_argument(
        "manifest", type=str, help="A list of files to copy, one per line"
    )
    parser.add_argument(
        "destination", type=str, help="The destination directory to copy files to"
    )
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    os.makedirs(args.destination, exist_ok=True)

    extract_files(
        args.manifest,
        args.include_different_extensions,
        args.dry_run,
        args.prefix,
        args.destination,
    )


def extract_files(manifest, include_different_extensions, dry_run, prefix, destination):
    with open(manifest, "r") as f:
        files = [file.strip() for file in f]

    for file in files:
        filebase, _ = os.path.splitext(os.path.basename(file))
        dirname = os.path.dirname(file)
        candidates = (
            [file]
            if not include_different_extensions
            else glob.glob(f"{dirname}/{filebase}.*")
        )
        for candidate in candidates:
            # Proceed only if the file is a relative path or if prefix is specified and the file starts with the prefix
            if os.path.isabs(candidate) and not prefix:
                logging.info(f"Skipping {file} because it is an absolute path. Specify a prefix to allow absolute paths.")
                continue
            if prefix and not candidate.startswith(prefix):
                logging.info(f"Skipping {file} because it does not start with {prefix}")
                continue
            if not os.path.exists(candidate):
                logging.info(f"Skipping {file} because it does not exist")
                continue

            
            relative_path = os.path.relpath(candidate, prefix) if prefix else candidate
            dest_path = os.path.join(destination, relative_path)
            if not dry_run:
                parent = os.path.dirname(dest_path)
                if parent:
                    os.makedirs(parent, exist_ok=True)
                shutil.copy(candidate, dest_path)
            logging.info(f"{candidate} -> {dest_path}")


if __name__ == "__main__":
    sys.exit(main())
