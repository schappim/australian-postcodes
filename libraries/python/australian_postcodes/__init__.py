"""Australian postcode + suburb lookup, with bundled data."""

from __future__ import annotations

import csv
from dataclasses import dataclass, asdict
from importlib import resources
from typing import Iterable, List, Optional

__version__ = "2026.5.27"
__all__ = [
    "Record",
    "STATES",
    "all_records",
    "find_by_postcode",
    "find_by_suburb",
    "postcode_for",
    "all_in_state",
    "reload",
]

STATES = ("ACT", "NSW", "NT", "QLD", "SA", "TAS", "VIC", "WA")


@dataclass(frozen=True)
class Record:
    postcode: str
    suburb: str
    state: str
    lat: str
    lon: str
    category: str

    def to_dict(self) -> dict:
        return asdict(self)


_records: Optional[List[Record]] = None
_by_postcode: Optional[dict] = None
_by_suburb: Optional[dict] = None
_by_state: Optional[dict] = None


def _load() -> List[Record]:
    global _records, _by_postcode, _by_suburb, _by_state
    if _records is not None:
        return _records
    with resources.files("australian_postcodes.data").joinpath(
        "australian-postcodes.csv"
    ).open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    recs: List[Record] = [
        Record(
            postcode=r["Postcode"],
            suburb=r["Suburb"],
            state=r["State"],
            lat=r["Lat"],
            lon=r["Lon"],
            category=r["Category"],
        )
        for r in rows
    ]
    _by_postcode = {}
    _by_suburb = {}
    _by_state = {}
    for r in recs:
        _by_postcode.setdefault(r.postcode, []).append(r)
        _by_suburb.setdefault(r.suburb.upper(), []).append(r)
        _by_state.setdefault(r.state, []).append(r)
    _records = recs
    return recs


def reload() -> List[Record]:
    """Drop the cached dataset and reload from disk."""
    global _records, _by_postcode, _by_suburb, _by_state
    _records = _by_postcode = _by_suburb = _by_state = None
    return _load()


def all_records() -> List[Record]:
    """Every record in the dataset."""
    return list(_load())


def find_by_postcode(postcode) -> List[Record]:
    """All records matching a 4-digit postcode."""
    _load()
    key = str(postcode).rjust(4, "0")
    return list(_by_postcode.get(key, []))  # type: ignore[arg-type]


def find_by_suburb(suburb: str, state: Optional[str] = None) -> List[Record]:
    """All records matching a suburb (case-insensitive). Narrow by state."""
    _load()
    key = suburb.upper().strip()
    rows = list(_by_suburb.get(key, []))  # type: ignore[arg-type]
    if state:
        st = state.upper()
        rows = [r for r in rows if r.state == st]
    return rows


def postcode_for(suburb: str, state: str) -> Optional[str]:
    """First postcode for the (suburb, state) pair, or None."""
    rows = find_by_suburb(suburb, state=state)
    return rows[0].postcode if rows else None


def all_in_state(state: str) -> List[Record]:
    """Every record in a given state."""
    _load()
    return list(_by_state.get(state.upper(), []))  # type: ignore[arg-type]
