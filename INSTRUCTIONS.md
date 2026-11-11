# Translations instructions

Package `ourapps-ae/translations` version `0.5.0`. It provides the `language` interface (type `ae/language`, version 1.0.0, OpenRPC 1.3.2 document `interfaces/language.json`; its `StringTable` schema is the shape of the string table) and the `resources` generator.

## For the agent

- Select this component when the application shows text in more than one language. Skip it for single-language applications.
- Connect the provided `language` port to every component that shows text (`guided-tour` requires it; the recipe's own screens use it directly).
- Setting: `languages` (string, label; optional; default `en fr de es`): the recipe's `languages` answer written as a space-separated list (for example `en fr`). English must be listed. No accounts or keys are needed.
- The generator accepts only `en`, `fr`, `de`, `es`; any other name is rejected before output is written. Pass the setting as `--languages`, or ship a table with every language and offer the languages of `web/languages.ts`, which aepm renders from the setting at install.
- Place the recipe's string table at a path the generator can read (`resources/strings.json`) and run the generator once per platform target the recipe includes.

## For the developer

- Install paths: `components/translations/web/i18n.ts`, `components/translations/apple/Sources/Language.swift`, `components/translations/android/src/main/java/ae/i18n/AppLanguage.kt`, `components/translations/scripts/generate.py`. The Kotlin package is `ae.i18n` and the web file is `i18n.ts`.
- Language selection: `selectLanguage(requested, supported, fallback)` returns the exact match, else the part before the first hyphen, else the fallback. Case is preserved (`fr-CA` against `["fr"]` gives `fr`).
- Lookup: `lookup(messages, key)` returns the stored text (an empty string counts as present) or the key itself.
- Dictionaries, persisted choice and the platform context belong to the application. This component stores nothing.
- String table: a JSON object of `key -> {en, fr, de, es}` (only the chosen languages are required). Keys start with a letter and contain letters, digits and underscores. Placeholders are `{name}`; every language must use the same set.
- Generate resources:

  `python3 components/translations/scripts/generate.py --strings resources/strings.json --web web/src --apple ios/Resources --android android/app/src/main/res --languages "en fr"`

  Without `--languages` all four are generated. Only the chosen languages are written; the string table must hold each of them (extra known languages are ignored).

  Outputs: `strings.json` (web), `Localizable.xcstrings` (Apple), `values/strings.xml` and `values-fr|de|es/strings.xml` for the chosen languages (Android). Native placeholders are numbered in English first-appearance order.
- Typed accessors are not generated; the application writes its own.

## How to check

From the component directory:

- `node --test tests/web.test.ts`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `python3 tests/native.py apple` (needs swiftc 6.4.2)
- `python3 tests/native.py android` (needs kotlinc 2.2.0 and java 26.0.1; not runnable where kotlinc is missing)
- `python3.12 -B tools/check_component.py components/translations` from the workspace root validates the manifest and sidecars and runs the required-local suites.

Verify in the application by switching to `fr-CA` with `["en","fr"]` supported and checking that French text appears, then by looking up a missing key and checking that the key is shown.
