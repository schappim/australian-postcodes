"use strict";

const fs = require("fs");
const path = require("path");

const DATA_PATH = path.join(__dirname, "data", "australian-postcodes.csv");
const STATES = ["ACT", "NSW", "NT", "QLD", "SA", "TAS", "VIC", "WA"];

let _records = null;
let _byPostcode = null;
let _bySuburb = null;
let _byState = null;

function parseCsv(text) {
  // The bundled CSV has no embedded commas/newlines/quotes — a tiny parser is fine.
  const lines = text.replace(/\r\n/g, "\n").split("\n");
  const header = lines.shift().split(",").map((h) => h.toLowerCase());
  const out = [];
  for (const line of lines) {
    if (!line) continue;
    const cols = line.split(",");
    const row = {};
    for (let i = 0; i < header.length; i++) {
      row[header[i]] = cols[i] !== undefined ? cols[i] : "";
    }
    out.push(row);
  }
  return out;
}

function load() {
  if (_records) return _records;
  const text = fs.readFileSync(DATA_PATH, "utf8");
  _records = parseCsv(text);
  _byPostcode = new Map();
  _bySuburb = new Map();
  _byState = new Map();
  for (const r of _records) {
    pushTo(_byPostcode, r.postcode, r);
    pushTo(_bySuburb, r.suburb.toUpperCase(), r);
    pushTo(_byState, r.state, r);
  }
  return _records;
}

function pushTo(map, key, value) {
  const list = map.get(key);
  if (list) list.push(value); else map.set(key, [value]);
}

function all() {
  return load().slice();
}

function findByPostcode(postcode) {
  load();
  const key = String(postcode).padStart(4, "0");
  return (_byPostcode.get(key) || []).slice();
}

function findBySuburb(suburb, opts = {}) {
  load();
  const key = String(suburb).toUpperCase().trim();
  let rows = (_bySuburb.get(key) || []).slice();
  if (opts.state) {
    const st = String(opts.state).toUpperCase();
    rows = rows.filter((r) => r.state === st);
  }
  return rows;
}

function postcodeFor(suburb, state) {
  const rows = findBySuburb(suburb, { state });
  return rows[0] ? rows[0].postcode : null;
}

function allInState(state) {
  load();
  return (_byState.get(String(state).toUpperCase()) || []).slice();
}

function reload() {
  _records = null;
  _byPostcode = null;
  _bySuburb = null;
  _byState = null;
  return load();
}

module.exports = {
  STATES,
  all,
  findByPostcode,
  findBySuburb,
  postcodeFor,
  allInState,
  reload,
};
