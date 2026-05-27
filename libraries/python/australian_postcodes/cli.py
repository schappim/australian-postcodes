"""Command-line interface: `australian-postcodes <subcommand> ...`"""

from __future__ import annotations

import argparse
import json
import sys

from . import (
    __version__,
    all_in_state,
    find_by_postcode,
    find_by_suburb,
    postcode_for,
)


def _dump(records):
    print(json.dumps([r.to_dict() for r in records], indent=2))


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="australian-postcodes")
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="cmd", required=True)

    p_pc = sub.add_parser("by-postcode", help="Look up by 4-digit postcode")
    p_pc.add_argument("postcode")

    p_sb = sub.add_parser("by-suburb", help="Look up by suburb name")
    p_sb.add_argument("suburb")
    p_sb.add_argument("--state", help="Narrow to a state (e.g. NSW)")

    p_st = sub.add_parser("in-state", help="All records for one state")
    p_st.add_argument("state")

    p_pf = sub.add_parser("postcode-for", help="One postcode for a suburb+state")
    p_pf.add_argument("suburb")
    p_pf.add_argument("state")

    args = p.parse_args(argv)

    if args.cmd == "by-postcode":
        _dump(find_by_postcode(args.postcode))
    elif args.cmd == "by-suburb":
        _dump(find_by_suburb(args.suburb, state=args.state))
    elif args.cmd == "in-state":
        _dump(all_in_state(args.state))
    elif args.cmd == "postcode-for":
        result = postcode_for(args.suburb, args.state)
        if result is None:
            print("", file=sys.stderr)
            return 1
        print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
