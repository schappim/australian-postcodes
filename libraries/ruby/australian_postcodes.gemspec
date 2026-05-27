# frozen_string_literal: true

require_relative "lib/australian_postcodes/version"

Gem::Specification.new do |s|
  s.name = "australian_postcodes"
  s.version = AustralianPostcodes::VERSION
  s.summary = "Australian postcode + suburb lookup, with bundled data"
  s.description = <<~DESC
    Pure-Ruby lookup library for Australian postcodes, suburbs, and
    states. The dataset (16,511 rows) is bundled with the gem — no
    network or external dependencies required.
  DESC
  s.authors = ["schappim"]
  s.homepage = "https://github.com/schappim/australian-postcodes"
  s.license = "MIT"

  s.required_ruby_version = ">= 2.7"

  s.files = Dir["lib/**/*.rb", "data/australian-postcodes.csv", "README.md", "LICENSE*"]
  s.require_paths = ["lib"]
end
