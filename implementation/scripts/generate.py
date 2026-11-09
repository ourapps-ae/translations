#!/usr/bin/env python3
"""Generate platform resources from an injected four-language string table."""
import argparse
import json
import re
from pathlib import Path
from xml.sax.saxutils import escape

LANGS = ("en", "fr", "de", "es")


def order(text):
    return list(dict.fromkeys(re.findall(r"\{(\w+)\}", text)))


def android(text, names):
    out = text.replace("%", "%%")
    for i, name in enumerate(names, 1):
        out = out.replace("{" + name + "}", f"%{i}$s")
    out = out.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"').replace("\n", "\\n")
    return escape(out)


def ios(text, names):
    out = text.replace("%", "%%")
    for i, name in enumerate(names, 1):
        out = out.replace("{" + name + "}", f"%{i}$@")
    return out


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate string key")
        result[key] = value
    return result


def parse_languages(text):
    """A space-separated installer setting such as "en fr" to a tuple; English is the source and must be listed."""
    wanted = tuple(text.split())
    if not wanted or len(set(wanted)) != len(wanted) or any(lang not in LANGS for lang in wanted) or "en" not in wanted:
        raise ValueError("languages must be distinct names from en fr de es and include en")
    return wanted


def generate(strings, web, apple, android_root, languages=LANGS):
    languages = tuple(languages)
    if not languages or len(set(languages)) != len(languages) or any(lang not in LANGS for lang in languages) or "en" not in languages:
        raise ValueError("languages must be distinct names from en fr de es and include en")
    if not isinstance(strings, dict) or not strings:
        raise ValueError("string table must be a nonempty object")
    for key, translations in strings.items():
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", key):
            raise ValueError("invalid resource key")
        if not isinstance(translations, dict) or not set(languages) <= set(translations) <= set(LANGS):
            raise ValueError("each key requires " + ", ".join(languages) + " and no other language than en, fr, de, es")
        if any(not isinstance(translations[lang], str) for lang in languages):
            raise ValueError("translations must be strings")
        names = set(order(translations["en"]))
        if any(set(order(translations[lang])) != names for lang in languages):
            raise ValueError("translation placeholder mismatch: " + key)
    for lang in languages:
        destination = android_root / ("values" if lang == "en" else f"values-{lang}")
        destination.mkdir(parents=True, exist_ok=True)
        lines = ['<?xml version="1.0" encoding="utf-8"?>', "<resources>"]
        for key, translations in strings.items():
            lines.append(f'    <string name="{key}">{android(translations[lang], order(translations["en"]))}</string>')
        (destination / "strings.xml").write_text("\n".join(lines + ["</resources>"]) + "\n", encoding="utf-8")
    catalogue = {"sourceLanguage": "en", "version": "1.0", "strings": {}}
    for key, translations in strings.items():
        catalogue["strings"][key] = {
            "extractionState": "manual",
            "localizations": {lang: {"stringUnit": {"state": "translated", "value": ios(translations[lang], order(translations["en"]))}} for lang in languages},
        }
    apple.mkdir(parents=True, exist_ok=True)
    web.mkdir(parents=True, exist_ok=True)
    (apple / "Localizable.xcstrings").write_text(json.dumps(catalogue, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (web / "strings.json").write_text(json.dumps({lang: {key: value[lang] for key, value in strings.items()} for lang in languages}, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("strings", "web", "apple", "android"):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--languages", default=" ".join(LANGS), help='space-separated, for example "en fr"; default all four')
    args = parser.parse_args()
    generate(json.loads(args.strings.read_text(encoding="utf-8"), object_pairs_hook=unique), args.web, args.apple, args.android, parse_languages(args.languages))


if __name__ == "__main__":
    main()
