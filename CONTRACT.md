# Translations component

## Purpose and facilities
Lets an application speak English, French, German and Spanish, and pick the right one for each person. It does two jobs. At run time it chooses a language: a person whose device says `fr-CA` gets Canadian French if the application has it, otherwise French, otherwise the application's default language; and it looks up each piece of text in that language, showing the text's key when a translation is missing so the gap is visible rather than blank. At build time a generator takes one table of all the application's text, checks it, and writes the files each platform reads: `strings.json` for the web, `Localizable.xcstrings` for Apple and `strings.xml` for Android. It refuses a table where a translation is missing or where the translations do not use the same placeholders (such as `{name}`), so a French message can never drop the player's name that the English one shows.

The application writes the text; this component only chooses, checks and delivers it.

Facilities: `language` (Chooses each person's language and looks up the application's text in English, French, German or Spanish), `resources` (Checks the application's text table and writes the web, Apple and Android text files for the chosen languages).

## User inputs
The installer collects one setting:

- `languages`: the languages the application offers, separated by spaces (optional; default `en fr de es`). Allowed names are `en` (English), `fr` (French), `de` (German) and `es` (Spanish), each at most once, and `en` must be among them, because English is the language every text is written in first. For example `en fr` offers English and French only.

The installed web client reads the setting from `web/languages.ts`, and the generator takes it as `--languages`. The application supplies its own text table and remembers each person's choice.

## Artefacts and dependencies
`component.json` maps every `implementation/` source into `components/translations/`: `web/i18n.ts` (choosing and looking up), `web/languages.ts` (the `languages` setting, which clod writes at install), `apple/Sources/Language.swift`, the Android `com.clodhub.i18n` sources and `scripts/generate.py` (the generator). Python 3.12 and Node 26.5 with their standard libraries only. `tools.lock.json` pins the check tools (Node 26.5, Python 3.12, Swift 6.4, Kotlin 2.2, Java 26.0).

## Provided interfaces
`interfaces/language.json` defines `language` (`com.clodhub/language`) version 1.0.0 (facility id `language`) as an OpenRPC 1.3.2 document: `selectLanguage`, `lookup`, `parseLanguages` and the Python `generate`, each naming its Swift and Kotlin form, with the message map, the text table, the generated web `strings.json` and the `languages` setting as JSON Schema 2020-12 under `components.schemas`.

## Required interfaces
None from other components. The application supplies the text table, the list of languages it offers (from the setting), the language a person chose, and how text with placeholders is filled in.

## Integration
Write all the application's text in one table, `resources/strings.json`, where each key maps to its text in each offered language:

```json
{ "welcome": { "en": "Hello {name}", "fr": "Bonjour {name}", "de": "Hallo {name}", "es": "Hola {name}" } }
```

Keys start with a letter and hold letters, digits and underscores. Then generate the platform files:

```
python3 components/translations/scripts/generate.py --strings resources/strings.json --web web/src --apple ios/Resources --android android/app/src/main/res --languages "en fr de es"
```

On the web, `selectLanguage(navigator.language, parseLanguages(languages), "en")` picks the language and `lookup(messages, "welcome")` returns the text. On Apple use `Language.swift`; on Android import the `com.clodhub.i18n` functions (`AppLanguage`). Native placeholders are numbered in the order they first appear in English; web placeholders keep their names.

## Visual definition and connected examples
`visual/definition.json` declares the `language` output; `visual/examples/connected.json` connects it to an illustrative application consumer. Both image formats and their text description are in `visual/output/`.

## Infrastructure
None. No account, service or network access; the generator writes only the folders it is given.

## Verification
`node --test tests/web.test.ts` (required) checks language choice (exact, then the base language, then the fallback), lookup including empty text and missing keys, the `languages` setting, and that the interface document matches the code. `python3 -m unittest discover -s tests -p test_*.py` (required) runs the real generator: all four languages, escaping for each platform, and refusal of a missing translation, a duplicate key or mismatched placeholders before anything is written. `python3 tests/native.py apple` and `python3 tests/native.py android` compile the Swift and Kotlin forms and check them on the same cases.

## Scenarios and presentation
A Montreal player's phone is set to `fr-CA`; the application offers `en fr`, so the game appears in French. A Berlin player is set to `de-DE`; German is not offered, so the game appears in English. A developer adds a new message in English and French only; the generator stops with an error naming the missing German and Spanish text instead of shipping a gap. A French translator moves `{name}` to the end of a sentence; it still shows the right player's name.

## Updates and removal
Updates replace the component's files; it stores nothing. Removing it means removing its imports and the generated text files; each person's remembered language stays in the application's own storage.
