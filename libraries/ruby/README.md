# australian_postcodes (Ruby gem)

Lookup Australian postcodes, suburbs, and states from Ruby. The dataset
(16,511 rows) is bundled with the gem — no network, no external services.

## Install

### As a published gem

```sh
gem install australian_postcodes
```

```ruby
# Gemfile
gem "australian_postcodes"
```

### Directly from this repo (no RubyGems publish)

```ruby
# Gemfile — pin to a tag, branch, or commit
gem "australian_postcodes",
    git: "https://github.com/schappim/australian-postcodes.git",
    glob: "libraries/ruby/*.gemspec"

# Or, if you have it checked out locally:
gem "australian_postcodes", path: "../australian-postcodes/libraries/ruby"
```

Then `bundle install`.

## Usage

```ruby
require "australian_postcodes"

# Find by postcode (always an Array — one postcode can cover many suburbs)
AustralianPostcodes.find_by_postcode("2000")
# => [#<struct AustralianPostcodes::Record postcode="2000", suburb="SYDNEY", state="NSW", ...>]

# Find by suburb (case-insensitive)
AustralianPostcodes.find_by_suburb("melbourne")
# => [...VIC entry...]

# Narrow by state
AustralianPostcodes.find_by_suburb("Springfield", state: "QLD")

# The most common case — give me THE postcode for this suburb in this state
AustralianPostcodes.postcode_for("Sydney", "NSW")  # => "2000"

# Everything in a state
AustralianPostcodes.all_in_state("ACT").size      # => 151

# All records
AustralianPostcodes.all.size                       # => 16511
```

Each record is a `Struct` with `postcode, suburb, state, lat, lon, category`.

## Notes

- Postcode is a `String` (preserves leading zeros — `"0810"`, `"0200"`)
- Suburb names are UPPERCASE
- `category` is `"Delivery Area"` or `"Post Office Boxes"`
- Lat/Lon are approximate (3 dp) and may be empty for newer rows
