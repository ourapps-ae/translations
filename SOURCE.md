# Source mapping

Reference revision: `19905b75dbea89fbfd424d67fe26c81aaed0e018` (frozen McInPoker, read with `git show` in `mcinpoker/`). The OurPoker recipe now imports this component, so its copies are thin wrappers; ranges below are in the frozen revision. The `languages` option of `generate.py` (`parse_languages`, a `languages` argument) and `parseLanguages` in `i18n.ts` are new code with no frozen counterpart.

| Implementation file | Frozen source and lines | Generalised | Left behind |
|---|---|---|---|
| `implementation/scripts/generate.py` (81) | `i18n/generate.py` 1-64 | Paths are injected (`--strings --web --apple --android`); language set, key grammar, duplicate keys and placeholder mismatches are validated before any write; XML escaping added | The fixed repository paths and the game's key list (`i18n/keys.txt`, `i18n/strings.json`) |
| `implementation/web/i18n.ts` (9) | `web/src/i18n.ts` 11-43 (`LANGUAGES`, `pickLanguage`, `L`) | Exact, base-before-hyphen, then fallback selection and key lookup as pure functions with supplied lists | Browser storage, current-language state, placeholder formatting (`L`), game text (`promptText`, `eventText`, `roomName`, `actionText`, lines 44-68) |
| `implementation/android/src/main/java/ae/i18n/AppLanguage.kt` (15) | `android/app/src/main/java/com/georgemcintyre/mcinpoker/AppLanguage.kt` 11-31 (`AppLanguage`) | Selection and lookup only, in package `ae.i18n` | Shared-preferences storage, `Context` wrapping and locale lists (`picked`, `pick`, `current`, `wrap`) |
| `implementation/apple/Sources/Language.swift` (9) | `ios/McInPoker/Sources/Strings.swift` 6-36 (`Language`, `localized`) | Same selection and lookup contract as the web file | Observable singleton, bundle selection and `L` formatting, typed game accessors (lines 37-101) |

`implementation/web/languages.ts` is new (`generated-platform`): the `languages` setting as aepm renders it at install, for web clients that ship the generated table with every language.

Fixtures, `examples/consumer.ts` and tests are neutral local consumers written for this component. No game translation resources are included.

