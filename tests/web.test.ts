import assert from "node:assert/strict";
import test from "node:test";
import {selectLanguage, lookup, parseLanguages} from "../implementation/web/i18n.ts";
import {greeting} from "../examples/consumer.ts";

test("exact language precedes base and fallback", () => {
  assert.equal(selectLanguage("fr-CA", ["en", "fr", "fr-CA"], "en"), "fr-CA");
  assert.equal(selectLanguage("fr-CA", ["en", "fr"], "en"), "fr");
  for (const requested of ["", "zz", "FR", "-fr"]) assert.equal(selectLanguage(requested, ["en", "fr"], "en"), "en");
  assert.equal(selectLanguage("en", [], "de"), "de");
});

test("lookup preserves empty strings and misses inherited keys", () => {
  assert.equal(lookup({hello: "Bonjour"}, "hello"), "Bonjour");
  assert.equal(lookup({hello: ""}, "hello"), "");
  assert.equal(lookup({}, "missing"), "missing");
  assert.equal(lookup({}, "constructor"), "constructor");
});

test("independent consumer uses regional fallback", () => {
  assert.equal(greeting("fr-CA"), "Bonjour");
  assert.equal(greeting("ja"), "Hello");
});

test("the languages setting is a space-separated list of known distinct names", () => {
  assert.deepEqual(parseLanguages("en fr"), ["en", "fr"]);
  assert.deepEqual(parseLanguages("  en   de  es "), ["en", "de", "es"]);
  assert.deepEqual(parseLanguages("en fr de es"), ["en", "fr", "de", "es"]);
  for (const bad of ["", "   ", "en en", "en pt", "en,fr"]) assert.throws(() => parseLanguages(bad), /languages must be/);
  assert.deepEqual(parseLanguages("en fr-CA", ["en", "fr-CA"]), ["en", "fr-CA"]);
});
