# australian-postcodes (Python)

Lookup Australian postcodes, suburbs, and states from Python. The dataset
(16,511 rows) is bundled inside the package — no network calls, zero runtime
dependencies (stdlib only).

## Install

```sh
pip install australian-postcodes
```

Or from this repo directly:

```sh
pip install "git+https://github.com/schappim/australian-postcodes.git#subdirectory=libraries/python"
```

## Library usage

```python
import australian_postcodes as ap

# Find by postcode (always a list — one postcode can cover many suburbs)
ap.find_by_postcode("2000")
# [Record(postcode='2000', suburb='SYDNEY', state='NSW', lat='-33.860', lon='151.210', category='Delivery Area'), ...]

# Find by suburb (case-insensitive)
ap.find_by_suburb("melbourne")

# Narrow by state
ap.find_by_suburb("Springfield", state="QLD")

# The most common case — give me THE postcode
ap.postcode_for("Sydney", "NSW")      # '2000'

# Everything in a state
len(ap.all_in_state("ACT"))            # 151

# All records
len(ap.all_records())                  # 16511
```

Each `Record` is a frozen `dataclass` with `postcode, suburb, state, lat, lon, category`.

## CLI

The package installs an `australian-postcodes` script:

```sh
australian-postcodes by-postcode 2000
australian-postcodes by-suburb Sydney --state NSW
australian-postcodes in-state ACT
australian-postcodes postcode-for Melbourne VIC   # -> 3000
```

All commands return JSON except `postcode-for` which prints the bare string.

## Notes

- `postcode` is a `str` (preserves leading zeros — `"0810"`, `"0200"`)
- Suburb names are UPPERCASE
- `category` is `"Delivery Area"` or `"Post Office Boxes"`
- Lat/Lon are approximate (3 dp) and may be empty for newer rows
