#!/usr/bin/env python3

'''
Convert the specified columns in a csv file from doy (with time) to yyyy-mm-ddTHH:MM:SS
'''

import argparse
import csv
import datetime
import sys

def main():
    parser = argparse.ArgumentParser(description='Convert the specified columns in a csv file from doy to yyyy-mm-dd')
    parser.add_argument('input_file', type=str, help='The input csv file')
    parser.add_argument('output_file', type=str, help='The output csv file')
    parser.add_argument('--output-format', type=str, help='The format of the datetime to convert to', default='%Y-%m-%dT%H:%M:%S')
    parser.add_argument('--input-format', type=str, help='The format of the datetime to convert from', default='%Y-%jT%H:%M:%S')
    parser.add_argument('--header', action='store_true', help='The header row is the first row of the csv file')
    parser.add_argument('--columns', type=int, nargs='+', help='The column numbers to convert', required=True)
    args = parser.parse_args()

    #verify that the columns are in range, and correspond to doy (with time)
    validate(args)
    do_conversion(args.input_file, args.output_file, args.columns, args.input_format, args.output_format, args.header)

def validate(args):
    """Validate the arguments"""
    #verify that there are columns to convert
    if len(args.columns) == 0:
        print("No columns to convert")
        sys.exit(1)

    with open(args.input_file, 'r') as input_file:
        reader = csv.reader(input_file)
        if args.header:
            _ = next(reader)
        row = next(reader)

    if any(column < 0 or column >= len(row) for column in args.columns):
        out_of_range_columns = [column for column in args.columns if column < 0 or column >= len(row)]
        print(f"Columns must be within the range of the csv file. Columns {out_of_range_columns} are out of range")
        sys.exit(1)
    for column in args.columns:
        try:
            datetime.datetime.strptime(row[column], args.input_format)
        except ValueError:
            print(f"Column {column} must be a {args.input_format} formatted datetime")
            sys.exit(1)

def do_conversion(input_file, output_file, columns, input_format, output_format, header):
    """Convert the specified columns in a csv file from the input format to the output format"""
    with open(input_file, 'r') as input_file, open(output_file, 'w') as output_file:
        reader = csv.reader(input_file)
        writer = csv.writer(output_file)
        if header:
            writer.writerow(next(reader))
        for row in reader:
            for column in columns:
                row[column] = datetime.datetime.strptime(row[column], input_format).strftime(output_format)
            writer.writerow(row)

if __name__ == '__main__':
    main()
