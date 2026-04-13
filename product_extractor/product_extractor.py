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

    with open(args.manifest, "r") as f:
        files = [file.strip() for file in f]

    for file in files:
        filebase, _ = os.path.splitext(os.path.basename(file))
        dirname = os.path.dirname(file)
        candidates = (
            [file]
            if not args.include_different_extensions
            else glob.glob(f"{dirname}/{filebase}.*")
        )
        for candidate in candidates:
            logging.info(f"Processing {candidate}")
            if args.prefix:
                if not candidate.startswith(args.prefix):
                    logging.info(
                        f"Skipping {file} because it does not start with {args.prefix}"
                    )
                    continue
                relative_path = os.path.relpath(candidate, args.prefix)
            else:
                relative_path = candidate
            destination = os.path.join(args.destination, relative_path)
            logging.info(
                f"Relative path: {relative_path}, destination: {destination}, args.destination: {args.destination}"
            )
            if not args.dry_run:
                shutil.copy(candidate, destination)
            logging.info(f"{candidate} -> {destination}")


if __name__ == "__main__":
    sys.exit(main())
