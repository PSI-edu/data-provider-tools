#! /usr/bin/env bash

# This will run multiple instances of the validator on a given directory, using xargs
# This should be faster than a single instance for CPU-bound tasks.
# Each validation worker will have its own output file, which will need to be reassembled later

set -e


usage()
{
    echo "usage: validate_parallel.sh validation_directory config_file catalog_file report_dir [workers] [batch_size]"
    exit 1
}


DIRNAME=$1
CONFIG_FILE=$2
CATALOG_FILE=$3
REPORT_DIR=$4
WORKERS=${5-4}
BATCH_SIZE=${6-1000}


[ -n "$DIRNAME" ] || (echo "Directory name not provided" && usage)
[ -d "$DIRNAME" ] || (echo "Directory name not a directory" && usage)

[ -n "$CONFIG_FILE" ] || (echo "Config file not provided" && usage)
[ -e "$CONFIG_FILE" ] || (echo "Config file does not exist" && usage)

[ -n "$CATALOG_FILE" ] || (echo "Catalog file not provided" && usage)
[ -e "$CATALOG_FILE" ] || (echo "Catalog file does not exist" && usage)

[ -n "$REPORT_DIR" ] || (echo "Report directory not provided" && usage)

# Not really a reliable way to find the validate worker script except to move into the directory first
# https://mywiki.wooledge.org/BashFAQ/028
[ -e "./validate_worker.sh" ] || (echo "Cannot find validate worker script. Please cd to the directory that contains this script" && exit 1)

mkdir -p "$REPORT_DIR/complete"

find "$DIRNAME" -name "*.xml" -print0 | xargs -0 -n"${BATCH_SIZE}" -P"${WORKERS}" ./validate_worker.sh "$CONFIG_FILE" "$CATALOG_FILE" "$REPORT_DIR"

echo "Done."
