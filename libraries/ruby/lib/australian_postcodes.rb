# frozen_string_literal: true

require "csv"
require_relative "australian_postcodes/version"

module AustralianPostcodes
  Record = Struct.new(:postcode, :suburb, :state, :lat, :lon, :category, keyword_init: true) do
    def to_h
      members.each_with_object({}) { |m, h| h[m] = self[m] }
    end
  end

  STATES = %w[ACT NSW NT QLD SA TAS VIC WA].freeze

  DATA_PATH = File.expand_path("../data/australian-postcodes.csv", __dir__)

  class << self
    # All records in the dataset (lazily loaded, cached).
    def all
      @all ||= load_records
    end

    # Reload the dataset from disk. Useful in tests.
    def reload!
      @all = nil
      @by_postcode = nil
      @by_suburb = nil
      @by_state = nil
      all
    end

    # Records matching a 4-digit postcode (string or int). A single postcode
    # can map to multiple suburbs; this always returns an Array.
    def find_by_postcode(postcode)
      key = postcode.to_s.rjust(4, "0")
      by_postcode[key] || []
    end

    # Records matching a suburb name (case-insensitive). Optionally narrow by
    # state code. The same suburb name can exist in several states; returns
    # an Array.
    def find_by_suburb(suburb, state: nil)
      key = suburb.to_s.upcase.strip
      records = by_suburb[key] || []
      return records if state.nil?
      st = state.to_s.upcase
      records.select { |r| r.state == st }
    end

    # Convenience: the first (or only) postcode for a (suburb, state) pair,
    # or nil if it does not exist. Use #find_by_suburb if you need them all.
    def postcode_for(suburb, state)
      r = find_by_suburb(suburb, state: state).first
      r && r.postcode
    end

    # All records in a given state.
    def all_in_state(state)
      by_state[state.to_s.upcase] || []
    end

    private

    def load_records
      CSV.read(DATA_PATH, headers: true).map do |row|
        Record.new(
          postcode: row["Postcode"],
          suburb: row["Suburb"],
          state: row["State"],
          lat: row["Lat"],
          lon: row["Lon"],
          category: row["Category"],
        )
      end.freeze
    end

    def by_postcode
      @by_postcode ||= all.group_by(&:postcode).freeze
    end

    def by_suburb
      @by_suburb ||= all.group_by(&:suburb).freeze
    end

    def by_state
      @by_state ||= all.group_by(&:state).freeze
    end
  end
end
