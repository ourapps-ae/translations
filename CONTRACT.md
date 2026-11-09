# Translations component

## Purpose and facilities
Package `ourapps-ae/translations` (interface type `ae/language`). `language` selects exact, base, then fallback languages and looks up text. `resources` generates resources for the chosen languages of English, French, German and Spanish with matching placeholder sets.

## User inputs
One setting: `languages` (string, label grammar; optional; default `en fr de es`), a space-separated list of the languages to generate and offer; English must be listed. The generator takes it as `--languages` and `parseLanguages` checks it in code. Callers supply supported languages, fallback, message maps and four explicit generator paths. No secrets or application resources are bundled.

## Artefacts and dependencies
See `component.json` for each `implementation/` source mapped into `components/translations/`. Python 3.12.8 and Node 26.5.0 require only their standard libraries. Native consumers require Swift 6.4.2 or Kotlin 2.2.0 and Java 26.0.1; declared platform checks distinguish availability. `tools.lock.json` pins verification tools. Licence wording remains deferred.

## Provided interfaces
`interfaces/language.json` defines `language` version 1.0.0 (facility id `language`). `selectLanguage` preserves case and checks exact language before its first hyphen-separated base; unsupported values return the supplied fallback. `lookup` returns a present value, including empty text, or the requested key. `parseLanguages` turns the `languages` setting into a checked list.

## Required interfaces
The application supplies its own dictionaries, supported language list, persisted selection and platform context. It owns typed resource accessors and placeholder formatting.

## Integration
See `INSTRUCTIONS.md` for selection and configuration, and `suitability.json` for the (library-only) profile. Import `web/i18n.ts`, include `apple/Sources/Language.swift`, or add the Android source root and import `ae.i18n` functions. `AppLanguage` also exposes Kotlin object methods. Run `python3 components/translations/scripts/generate.py --strings resources/strings.json --web web/src --apple ios/Resources --android android/app/src/main/res`. The input maps resource keys to exactly `en`, `fr`, `de`, `es` strings. Keys start with a letter and contain mixed-case letters, digits and underscores; every platform preserves their exact spelling. Output is `strings.json`, `Localizable.xcstrings` and `values*/strings.xml`. Invalid language sets, duplicate keys or placeholder mismatches fail before writing output. Numbered native placeholders follow English first-appearance order; browser placeholders remain named. No typed accessors are generated.

## Visual definition and connected examples
`visual/definition.json` declares the `language` output; `visual/examples/connected.json` connects it to an illustrative application consumer. Vector and raster images and their text description are in `visual/output/`.

## Infrastructure
No account, deployed service or network access is needed. Generation writes only caller-selected resource directories. Costs are unmeasured.

## Verification

Execution prerequisites are empty for these local library checks. Coverage is described here and in facilities; installed compilers are checked through the manifest's tools declaration.
`node --test tests/web.test.ts` covers language selection, lookup and the independent consumer. `python3 -m unittest discover -s tests -p test_*.py` covers real generator invocation, four-language outputs, escaping and invalid input. `python3 tests/native.py apple` and `python3 tests/native.py android` compile and run the retained native consumers. Native checks do not establish device integration. Fixtures and tool pins travel with the archive.

## Scenarios and presentation
`fr-CA` uses an exact supplied dictionary, else French, else fallback. Missing keys display their keys. Reordered placeholders retain the original argument identity. The connected diagram shows the component providing language lookup to application-owned text rendering.

## Updates and removal
Patch updates replace owned source files. The `languages` setting (default `en fr de es`) feeds `parseLanguages` and the generator option `--languages`. No persisted state is owned. Remove the source imports and generated resources when removing the component; application-owned preferences remain.
