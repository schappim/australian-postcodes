# australian-postcodes (Node / npm)

Lookup Australian postcodes, suburbs, and states from Node.js. The dataset
(16,511 rows) ships inside the package — no network calls, zero runtime
dependencies.

## Install

### As a published npm package

```sh
npm install australian-postcodes
# or
yarn add australian-postcodes
# or
pnpm add australian-postcodes
```

### Directly from this repo

```sh
npm install github:schappim/australian-postcodes#master --prefix /your/app
```

…and point at `libraries/javascript`, or copy that folder into your project.

## Usage

```js
const ap = require("australian-postcodes");

// Find by postcode (always an Array — one postcode can cover many suburbs)
ap.findByPostcode("2000");
// => [{ postcode: "2000", suburb: "SYDNEY", state: "NSW", lat: "-33.860", lon: "151.210", category: "Delivery Area" }, ...]

// Find by suburb (case-insensitive)
ap.findBySuburb("melbourne");

// Narrow by state
ap.findBySuburb("Springfield", { state: "QLD" });

// The most common case — give me THE postcode for this suburb in this state
ap.postcodeFor("Sydney", "NSW");      // => "2000"

// Everything in a state
ap.allInState("ACT").length;          // => 151

// All records
ap.all().length;                      // => 16511
```

ESM:

```js
import { findByPostcode, postcodeFor } from "australian-postcodes";
```

TypeScript types are bundled (`index.d.ts`).

## Notes

- `postcode` is a **string** (preserves leading zeros — `"0810"`, `"0200"`)
- Suburb names are UPPERCASE in the data
- `category` is `"Delivery Area"` or `"Post Office Boxes"`
- Lat/Lon are approximate (3 dp) and may be empty for newer rows
