# Australian Postcodes & Suburbs

A clean, machine-readable list of every Australian postcode + suburb / locality.

- **16,511 rows** across all 8 states and territories
- Updated **2026-05-27**
- Available as CSV, TSV, JSON, and Markdown — at the full level, per-state, or by postcode prefix
- Approximate Lat/Lon carried over from the 2021 snapshot for the 15,599 rows where the (postcode, suburb, state) key still matches; 912 rows new in 2026 have empty coordinates
- MIT-spirit "as-is" licence — see the bottom of this file

## Quick links

| I want…                                       | File                                                                             |
|-----------------------------------------------|----------------------------------------------------------------------------------|
| **Everything**, with coordinates and category | [`australian-postcodes.csv`](australian-postcodes.csv)                           |
| Everything as TSV                             | [`australian-postcodes.tsv`](australian-postcodes.tsv)                           |
| Everything as JSON                            | [`australian-postcodes.json`](australian-postcodes.json)                         |
| Just one state                                | [`data/by-state/<STATE>.csv`](data/by-state/) (csv / json / md)                  |
| Just suburb→postcode (no coords)              | [`data/lookup/postcodes-lookup.csv`](data/lookup/postcodes-lookup.csv)           |
| Just suburb→postcode for one state            | [`data/lookup/by-state/<STATE>.csv`](data/lookup/by-state/)                      |
| Lookup by postcode region                     | [`data/by-postcode-prefix/<0-9>.csv`](data/by-postcode-prefix/)                  |
| Today's snapshot, immutably dated             | [`australian-postcodes-2026-05-27.csv`](australian-postcodes-2026-05-27.csv)     |
| 2021 historical snapshot                      | [`australian-postcodes-2021-04-23.csv`](australian-postcodes-2021-04-23.csv)     |

See [`data/README.md`](data/README.md) for the full directory map.

## Schema (main files)

| Column     | Type   | Example          | Notes                                                     |
|------------|--------|------------------|-----------------------------------------------------------|
| `Postcode` | string | `2000`           | 4 digits, leading zeros preserved (`0810`, `0200`)        |
| `Suburb`   | string | `SYDNEY`         | Suburb / locality name, UPPERCASE                         |
| `State`    | enum   | `NSW`            | One of `ACT, NSW, NT, QLD, SA, TAS, VIC, WA`              |
| `Lat`      | string | `-33.860`        | Approximate latitude (3 dp), empty for some new rows      |
| `Lon`      | string | `151.210`        | Approximate longitude (3 dp), empty for some new rows     |
| `Category` | enum   | `Delivery Area`  | `Delivery Area` or `Post Office Boxes`                    |

> `Postcode` is a **string**, not an integer. Australian postcodes have leading zeros (e.g. `0810` for Darwin suburbs). If you load this into pandas, pass `dtype={'Postcode': str}` or use `parse_options=… string`.

## Row counts

| State | Rows  |
|-------|-------|
| NSW   | 4,836 |
| QLD   | 3,423 |
| VIC   | 3,187 |
| SA    | 1,946 |
| WA    | 1,845 |
| TAS   | 784   |
| NT    | 339   |
| ACT   | 151   |
| **Total** | **16,511** |

Of those, 16,237 are `Delivery Area` (actual residential / business localities) and 274 are `Post Office Boxes` ranges. Filter on `Category == "Delivery Area"` if you only want real suburbs.

## Examples

### CSV
```csv
Postcode,Suburb,State,Lat,Lon,Category
2601,ACTON,ACT,-35.280,149.110,Delivery Area
2602,AINSLIE,ACT,-35.260,149.150,Delivery Area
2914,AMAROO,ACT,-35.170,149.130,Delivery Area
2000,SYDNEY,NSW,-33.860,151.210,Delivery Area
3000,MELBOURNE,VIC,-37.810,144.960,Delivery Area
4000,BRISBANE,QLD,-27.470,153.020,Delivery Area
```

### JSON
```json
[
  {"postcode":"2000","suburb":"SYDNEY","state":"NSW","lat":"-33.860","lon":"151.210","category":"Delivery Area"},
  {"postcode":"3000","suburb":"MELBOURNE","state":"VIC","lat":"-37.810","lon":"144.960","category":"Delivery Area"}
]
```

### Python (pandas)
```python
import pandas as pd
df = pd.read_csv("australian-postcodes.csv", dtype={"Postcode": str})
df[df.State == "VIC"].head()
```

### Python (per-state, minimum memory)
```python
import pandas as pd
vic = pd.read_csv("data/by-state/VIC.csv", dtype={"Postcode": str})
```

### JavaScript / TypeScript
```ts
import data from "./data/by-state/NSW.json" assert { type: "json" };
const sydney = data.filter(r => r.suburb === "SYDNEY");
```

### Shell (suburb → postcode)
```sh
grep -F ',MELBOURNE,VIC,' australian-postcodes.csv
# or, much smaller file:
grep -F ',MELBOURNE' data/lookup/by-state/VIC.csv
```

## AI-friendly slices

If you are loading this data into an LLM prompt, prefer the smallest slice that
covers your query — every byte you avoid is tokens you avoid:

| Use case                                  | Recommended file                              | Approx size |
|-------------------------------------------|-----------------------------------------------|-------------|
| Whole country, full schema                | `australian-postcodes.csv`                    | 822 KB      |
| Whole country, no coords/category         | `data/lookup/postcodes-lookup.csv`            | 339 KB      |
| One state, full schema                    | `data/by-state/<STATE>.csv`                   | 7 KB – 244 KB |
| One state, just suburb+postcode           | `data/lookup/by-state/<STATE>.csv`            | 2 KB – 82 KB  |
| Postcode region (e.g. all 3xxx)           | `data/by-postcode-prefix/<0-9>.csv`           | 0.3 KB – 247 KB |
| Markdown table for inline reading         | `data/by-state/<STATE>.md`                    | 8 KB – 278 KB   |

ACT alone is ~150 rows and 2 KB — vastly cheaper to load than the full 16k-row file.

## Contributions

Pull requests welcome — particularly for:

- Filling in missing Lat/Lon on the 912 rows new in 2026
- Adding alternative slices (`by-postcode-2digit`, `by-LGA`, …) that consumers ask for
- Cleaning up suburb casing if your downstream prefers Title Case

When refreshing for a future release, please drop a dated snapshot
(`australian-postcodes-YYYY-MM-DD.csv`) so prior snapshots stay reproducible.

## Snapshots

- **2026-05-27** — Current dataset (`australian-postcodes-2026-05-27.*`)
- **2021-04-23** — Earlier snapshot, preserved as `australian-postcodes-2021-04-23.*`
- Lat/Lon coordinates are carried over from the 2021 dataset, matched by `(postcode, suburb, state)` key

## License

THE DATA IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE DATA OR THE USE OR OTHER DEALINGS IN THE DATA.
