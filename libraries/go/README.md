# australian-postcodes (Go)

Self-contained Go library + CLI for Australian postcode, suburb, and state
lookup. The dataset (16,511 rows) is **embedded into the binary** with
`go:embed`, so there are no runtime file dependencies and you can drop the
single executable onto any machine.

## Install (CLI)

```sh
go install github.com/schappim/australian-postcodes/libraries/go@latest
# installs a 'go' binary; rename or symlink it if you'd like 'postcodes':
mv ~/go/bin/go ~/go/bin/postcodes
```

Or build from a local checkout:

```sh
cd libraries/go
go build -o postcodes .
./postcodes by-postcode 2000
```

## CLI usage

```sh
postcodes by-postcode 2000
postcodes by-suburb --state NSW Sydney
postcodes in-state ACT
postcodes postcode-for Melbourne VIC      # -> 3000
```

All commands except `postcode-for` print JSON to stdout. `postcode-for` prints
the bare postcode (exits 1 if no match).

## Library usage

```go
import "github.com/schappim/australian-postcodes/libraries/go/postcodes"

rs := postcodes.FindByPostcode("2000")            // []postcodes.Record
rs := postcodes.FindBySuburb("Sydney", "NSW")     // []postcodes.Record
pc := postcodes.PostcodeFor("Melbourne", "VIC")   // "3000"
all := postcodes.AllInState("ACT")                // []postcodes.Record
```

Each `Record` has `Postcode, Suburb, State, Lat, Lon, Category` (all strings).

## Notes

- Postcode is a `string` (preserves leading zeros — `"0810"`, `"0200"`)
- Suburb names are UPPERCASE
- `Category` is `"Delivery Area"` or `"Post Office Boxes"`
- Lat/Lon are approximate (3 dp) and may be empty for newer rows
