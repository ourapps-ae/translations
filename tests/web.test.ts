import assert from "node:assert/strict";
import test from "node:test";
import { existsSync, readFileSync } from "node:fs";
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

test("the OpenRPC interface describes the language functions and the string table", async () => {
  const doc = JSON.parse(readFileSync(new URL("../interfaces/language.json", import.meta.url), "utf8"));
  assert.equal(doc.openrpc, "1.3.2");
  assert.deepEqual([doc.info.title, doc.info.version], ["ae/language", "1.0.0"]);
  const { LanguagesSetting, StringTable, Language } = doc.components.schemas;
  const setting = new RegExp(LanguagesSetting.pattern);
  assert.match(LanguagesSetting.default, setting);
  assert.deepEqual(parseLanguages(LanguagesSetting.default), Language.enum);
  for (const bad of ["", "en en", "en pt", "en,fr", "fr"]) assert.doesNotMatch(bad, setting, bad);
  const table = JSON.parse(readFileSync(new URL("fixtures/strings.json", import.meta.url), "utf8"));
  for (const [key, texts] of Object.entries(table)) {
    assert.match(key, new RegExp(StringTable.propertyNames.pattern));
    assert.deepEqual(Object.keys(texts as object).sort(), Object.keys(StringTable.additionalProperties.properties).sort());
  }
  const web: Record<string, unknown> = await import("../implementation/web/i18n.ts");
  for (const method of doc.methods) if (method.name !== "generate") assert.equal(typeof web[method.name], "function", method.name);
});

test("languages.ts is rendered by aepm at install from the languages setting, inside a quoted string", { skip: !existsSync(new URL("../component.json", import.meta.url)) && "component.json is not in this copy" }, () => {
  const manifest = JSON.parse(readFileSync(new URL("../component.json", import.meta.url), "utf8"));
  assert.deepEqual(manifest.artefacts.find((item: { source: string }) => item.source === "implementation/web/languages.ts"),
    { source: "implementation/web/languages.ts", destination: "components/translations/web/languages.ts", template: true, executable: false });
  const text = readFileSync(new URL("../implementation/web/languages.ts", import.meta.url), "utf8");
  assert.deepEqual([...text.matchAll(/"\{\{([A-Za-z]+)\}\}"/g)].map((match) => match[1]), ["languages"]);
  const rendered = text.replace("{{languages}}", manifest.collect.find((item: { id: string }) => item.id === "languages").default);
  assert.deepEqual(parseLanguages(/"([^"]+)"/.exec(rendered)![1]), ["en", "fr", "de", "es"]);
});
