#!/usr/bin/env python3
"""
simple script that combines product validation status with each error line to make
processing with grep easier

usage: ./flatten.py < report.txt
"""

import sys

def main():
    last_file = ""
    flattened = False
    
    for line in sys.stdin:
        trimmed = line.strip()
        if any(trimmed.startswith(x) for x in ["FAIL:", "PASS:"]):
            if not flattened:
                print(last_file)

            flattened = False
            last_file = trimmed
        elif any(trimmed.startswith(x) for x in ["ERROR", "WARNING"]):
            print(last_file, "---", trimmed)
            flattened = True
        else:
            print(trimmed)


if __name__ == "__main__":
    sys.exit(main())