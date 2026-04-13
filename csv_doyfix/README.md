# doyfix

`doyfix.py` converts selected columns in a CSV from **day-of-year (DOY) timestamps** to calendar datetimes (or other formats you choose).

Default input shape matches ISO-style DOY notation: `%Y-%jT%H:%M:%S` (for example `2024-001T12:30:00` for 1 January 2024 at 12:30:00). Default output is `%Y-%m-%dT%H:%M:%S` (for example `2024-01-01T12:30:00`).

## Requirements

- Python 3 (uses the standard library only: `argparse`, `csv`, `datetime`).

## Usage

```text
python3 doyfix.py INPUT_CSV OUTPUT_CSV --columns COL [COL ...] [--header] [--input-format FMT] [--output-format FMT]
```

### Arguments

| Argument | Description |
|----------|-------------|
| `INPUT_CSV` | Path to the source CSV. |
| `OUTPUT_CSV` | Path to write the converted CSV (created or overwritten). |
| `--columns` | **Required.** One or more column indices to rewrite. Indices are **0-based** (first data column is `0`). |
| `--header` | If set, the first row is copied through unchanged and only body rows are converted. |
| `--input-format` | `datetime.strptime` format for values in the selected columns. Default: `%Y-%jT%H:%M:%S`. |
| `--output-format` | `datetime.strftime` format written back to those columns. Default: `%Y-%m-%dT%H:%M:%S`. |

### Validation

Before writing the full file, the script opens the input, skips the header if `--header` is used, reads the **first data row**, and checks that:

- Every `--columns` index is in range for that row.
- Every selected cell parses successfully with `--input-format`.

If any check fails, the script prints an error and exits with status 1.

## Examples

Convert column 2 from default DOY-with-time to default calendar ISO-like datetime, preserving a header row:

```bash
python3 doyfix.py data_in.csv data_out.csv --header --columns 2
```

Convert several columns without a header:

```bash
python3 doyfix.py raw.csv fixed.csv --columns 0 3 5
```

Custom formats (still using Python’s format codes; `%j` is day-of-year 001–366):

```bash
python3 doyfix.py in.csv out.csv --columns 1 \
  --input-format '%Y-%j %H:%M:%S' \
  --output-format '%Y-%m-%d %H:%M:%S'
```

## Notes

- Parsing and writing use the CSV module with default dialect (comma-separated, standard quoting rules).
- Time zone is not handled: values are interpreted as naive local-style datetimes according to `datetime.strptime` / `strftime` behavior.
