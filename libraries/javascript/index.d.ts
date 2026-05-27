export interface PostcodeRecord {
  postcode: string;
  suburb: string;
  state: "ACT" | "NSW" | "NT" | "QLD" | "SA" | "TAS" | "VIC" | "WA" | string;
  lat: string;
  lon: string;
  category: "Delivery Area" | "Post Office Boxes" | string;
}

export interface FindBySuburbOptions {
  state?: string;
}

export const STATES: readonly string[];

export function all(): PostcodeRecord[];
export function findByPostcode(postcode: string | number): PostcodeRecord[];
export function findBySuburb(suburb: string, opts?: FindBySuburbOptions): PostcodeRecord[];
export function postcodeFor(suburb: string, state: string): string | null;
export function allInState(state: string): PostcodeRecord[];
export function reload(): PostcodeRecord[];
