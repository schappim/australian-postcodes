// Command postcodes is a CLI for Australian postcode / suburb / state lookups.
//
//	postcodes by-postcode 2000
//	postcodes by-suburb Sydney --state NSW
//	postcodes in-state ACT
//	postcodes postcode-for Melbourne VIC   # prints just the postcode
package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"

	"github.com/schappim/australian-postcodes/libraries/go/postcodes"
)

const usage = `postcodes — Australian postcode / suburb / state lookup

Usage:
  postcodes by-postcode <postcode>
  postcodes by-suburb [--state STATE] <suburb>
  postcodes in-state <state>
  postcodes postcode-for <suburb> <state>
`

func main() {
	if len(os.Args) < 2 {
		fmt.Fprint(os.Stderr, usage)
		os.Exit(2)
	}
	cmd := os.Args[1]
	args := os.Args[2:]
	switch cmd {
	case "by-postcode":
		if len(args) != 1 {
			fmt.Fprint(os.Stderr, usage)
			os.Exit(2)
		}
		dump(postcodes.FindByPostcode(args[0]))
	case "by-suburb":
		fs := flag.NewFlagSet("by-suburb", flag.ExitOnError)
		state := fs.String("state", "", "narrow to a specific state code (e.g. NSW)")
		_ = fs.Parse(args)
		if fs.NArg() != 1 {
			fmt.Fprint(os.Stderr, usage)
			os.Exit(2)
		}
		dump(postcodes.FindBySuburb(fs.Arg(0), *state))
	case "in-state":
		if len(args) != 1 {
			fmt.Fprint(os.Stderr, usage)
			os.Exit(2)
		}
		dump(postcodes.AllInState(args[0]))
	case "postcode-for":
		if len(args) != 2 {
			fmt.Fprint(os.Stderr, usage)
			os.Exit(2)
		}
		p := postcodes.PostcodeFor(args[0], args[1])
		if p == "" {
			os.Exit(1)
		}
		fmt.Println(p)
	case "-h", "--help", "help":
		fmt.Print(usage)
	default:
		fmt.Fprintf(os.Stderr, "unknown command %q\n\n%s", cmd, usage)
		os.Exit(2)
	}
}

func dump(rs []postcodes.Record) {
	enc := json.NewEncoder(os.Stdout)
	enc.SetIndent("", "  ")
	if err := enc.Encode(rs); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
