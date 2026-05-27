# `data/` directory

Smaller, sliced versions of the main `australian-postcodes.csv` so consumers
(especially AI agents that pay per token) can load just the slice they need.

## Layout

```
data/
├── by-state/                # full schema, split by State
│   ├── ACT.csv  ACT.json  ACT.md
│   ├── NSW.csv  NSW.json  NSW.md
│   ├── NT.csv   NT.json   NT.md
│   ├── QLD.csv  QLD.json  QLD.md
│   ├── SA.csv   SA.json   SA.md
│   ├── TAS.csv  TAS.json  TAS.md
│   ├── VIC.csv  VIC.json  VIC.md
│   └── WA.csv   WA.json   WA.md
├── by-postcode-prefix/      # split by first digit of Postcode
│   ├── 0.csv … 9.csv
└── lookup/                  # minimum-token suburb→postcode lookups
    ├── postcodes-lookup.csv         # Postcode,Suburb,State
    └── by-state/
        ├── ACT.csv … WA.csv         # Postcode,Suburb only
```

## Schemas

### `by-state/<STATE>.csv` (and `.json`)

Full schema, same as the root `australian-postcodes.csv`:

| Column   | Type     | Description                                                  |
|----------|----------|--------------------------------------------------------------|
| Postcode | string   | 4-digit Australian postcode (leading zeros preserved)        |
| Suburb   | string   | Suburb / locality name, UPPERCASE                            |
| State    | string   | 2–3-letter state code (ACT, NSW, NT, QLD, SA, TAS, VIC, WA)  |
| Lat      | string   | Approximate latitude (3 dp), or empty for rows new in 2026   |
| Lon      | string   | Approximate longitude (3 dp), or empty for rows new in 2026  |
| Category | string   | `Delivery Area` or `Post Office Boxes`                       |

### `by-state/<STATE>.md`

Markdown table version of the same rows, intended for human/AI readers that
prefer markdown over CSV.

### `by-postcode-prefix/<digit>.csv`

Same full schema, but bucketed by the first digit of the postcode. Useful when
you have a postcode but not a state. Rough mapping:

| Prefix | Region                                  |
|--------|-----------------------------------------|
| `0`    | NT & ACT specifics (e.g. ANU, Darwin)   |
| `1`    | NSW PO Box ranges                       |
| `2`    | NSW & ACT                               |
| `3`    | VIC                                     |
| `4`    | QLD                                     |
| `5`    | SA                                      |
| `6`    | WA                                      |
| `7`    | TAS                                     |
| `8`    | VIC PO Box ranges                       |
| `9`    | QLD large-volume ranges                 |

### `lookup/postcodes-lookup.csv`

Just `Postcode,Suburb,State`. ~339 KB (vs 822 KB for the full file). Use when
you do not need Lat/Lon/Category.

### `lookup/by-state/<STATE>.csv`

Just `Postcode,Suburb` — state is implied by the filename. ACT is **2 KB**.

## Row counts

| State | Rows |
|-------|------|
| ACT   | 151  |
| NSW   | 4,836 |
| NT    | 339  |
| QLD   | 3,423 |
| SA    | 1,946 |
| TAS   | 784  |
| VIC   | 3,187 |
| WA    | 1,845 |
| **Total** | **16,511** |
