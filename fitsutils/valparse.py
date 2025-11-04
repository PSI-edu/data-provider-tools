#!/usr/bin/env python3
"""
A tool to help determine how a value is stored. It reads in an entire column, and parses the value in multiple ways,
so a user can determine which is correct.

It tries every combination of

MSB/LSB
Signed/Unsigned
Converted/Unconverted (to or from signed)
"""
import argparse
import sys
import struct

ENDIANNESS = ('<', '>')
INT_SIZES = {
    8: ('b', 'B'),
    16: ('h', 'H'),
    32: ('i', 'I'),
    64: ('q', 'Q')
}
REAL_SIZES = {
    32: 'f',
    64: 'd'
}


def parse_ints(bits: int, value: bytes, endianness: str):
    """
    Parses a byte string in both signed and unsigned styles, and tries to convert them to the other style
    by applying an offset
    :param bits: The size of the byte pattern in bits
    :param value: The actual stored byte pattern
    :param endianness: MSB or LSB
    :return: A map containing both the unsigned and signed parse results, and the result of an attempt tp convert
    them to the other style
    """
    offset = 2**(bits - 1)

    signed_f, unsigned_f = INT_SIZES[bits]

    signed_v = struct.unpack(f'{endianness}{signed_f}', value)[0]
    unsigned_v = struct.unpack(f'{endianness}{unsigned_f}', value)[0]
    signed_to_unsigned_v = signed_v + offset
    unsigned_to_signed_v = unsigned_v - offset

    return {
        'offset': offset,
        'signed': signed_v,
        'unsigned': unsigned_v,
        'signed_to_unsigned': signed_to_unsigned_v,
        'unsigned_to_signed': unsigned_to_signed_v
    }


def parse_reals(bits: int, value: bytes):
    """
    Parses a byte string in both signed and unsigned styles, and tries to convert them to the other style
    by applying an offset
    :param bits: The size of the byte pattern in bits
    :param value: The actual stored byte pattern
    :param endianness: MSB or LSB
    :return: A map containing both the unsigned and signed parse results, and the result of an attempt tp convert
    them to the other style
    """
    fmt = REAL_SIZES[bits]

    msb = struct.unpack(f'>{fmt}', value)[0]
    lsb = struct.unpack(f'<{fmt}', value)[0]

    return {
        'msb': msb,
        'lsb': lsb,
        'hex': value.hex()
    }


def multiparse(bits: int, data_type: str, value: bytes):
    """
    Run the parser in both MSB and LSB style
    :param bits: The number of bits in the value
    :param value: The stored value to be processed
    :return: A map containing parse results for both MSB and LSB
    """
    if data_type == 'int':
        return {
            'msb': parse_ints(bits, value, '>'),
            'lsb': parse_ints(bits, value, '<')
        }
    else : 
        return parse_reals(bits, value)

def parse_file(fits_file, data_offset, records, record_length, field_position, field_size, data_type):
    """
    Reads in a column from a data table and tries to parse every value in a variety of ways, so a user can
    determine which is correct.

    Note: This uses *both* 0 and 1-based values. This is to make it easier to use values from a PDS4 label
    :param fits_file: The file to read in
    :param data_offset: The 0-based start byte of the data area
    :param records: The number of records to read in and parse
    :param record_length: The size of a record, in bytes
    :param field_position: The 1-based start byte of a field within a record
    :param field_size: The sie of the field, in bytes
    :return:
    """
    bits = field_size * 8

    with open(fits_file, 'rb') as f:
        f.read(data_offset)
        for _ in range(0, records):
            record = f.read(record_length)
            value = record[field_position-1:field_position+field_size-1]
            print(multiparse(bits, data_type, value))


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--field_length", type=int,
                        help="The size of the field to check, in bytes", required=True)
    parser.add_argument("--field_location", type=int,
                        help="The 1-based location of the field within the record", required=True)
    parser.add_argument("--offset", type=int, help="The 0-based start byte of the data table", required=True)
    parser.add_argument("--record_length", type=int, help="The length of each data record, in bytes", required=True)
    parser.add_argument("--records", type=int, help="The number of records to read", required=True)
    parser.add_argument("--data_type", type=str, help="The data type of the records, either real or int", required=True)

    parser.add_argument("fits_file")

    args = parser.parse_args()

    parse_file(args.fits_file, args.offset, args.records, args.record_length, args.field_location, args.field_length, args.data_type)

    return 0


if __name__ == '__main__':
    sys.exit(main())
