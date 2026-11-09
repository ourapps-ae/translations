import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("generate", ROOT / "implementation/scripts/generate.py")
generator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(generator)


class GenerationTests(unittest.TestCase):
    def setUp(self):
        self.strings = json.loads((ROOT / "tests/fixtures/strings.json").read_text())

    def test_real_command_outputs_all_platforms(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["python3", str(ROOT / "implementation/scripts/generate.py"), "--strings", str(ROOT / "tests/fixtures/strings.json"), "--web", str(root / "web"), "--apple", str(root / "apple"), "--android", str(root / "android")], check=True)
            tables = json.loads((root / "web/strings.json").read_text())
            self.assertEqual(set(tables), set(generator.LANGS))
            self.assertEqual(tables["fr"]["greeting"], self.strings["greeting"]["fr"])
            for language in generator.LANGS:
                folder = "values" if language == "en" else "values-" + language
                entries = ET.parse(root / "android" / folder / "strings.xml").getroot()
                text = entries.find("string[@name='greeting']").text
                self.assertIn("%1$s", text)
                self.assertIn("%2$s%%", text)
                self.assertIn("&", text)
            french = ET.parse(root / "android/values-fr/strings.xml").getroot()[0].text
            self.assertLess(french.index("%2$s"), french.index("%1$s"))
            catalogue = json.loads((root / "apple/Localizable.xcstrings").read_text())
            self.assertIn("%2$@%%", catalogue["strings"]["greeting"]["localizations"]["fr"]["stringUnit"]["value"])

    def test_bad_placeholders_fail_before_writes(self):
        self.strings["greeting"]["de"] = "Hallo {other}"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaisesRegex(ValueError, "placeholder"):
                generator.generate(self.strings, root / "web", root / "apple", root / "android")
            self.assertEqual(list(root.iterdir()), [])

    def test_mixed_case_keys_preserved_on_every_platform(self):
        keys = ["err_badInput", "act_saveAs", "p_waitingForInput", "label_A", "status_allReady"]
        strings = {key: {language: key for language in generator.LANGS} for key in keys}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            generator.generate(strings, root / "web", root / "apple", root / "android")
            web = json.loads((root / "web/strings.json").read_text())
            apple = json.loads((root / "apple/Localizable.xcstrings").read_text())
            self.assertEqual(set(apple["strings"]), set(keys))
            for language in generator.LANGS:
                self.assertEqual(set(web[language]), set(keys))
                folder = "values" if language == "en" else "values-" + language
                resources = ET.parse(root / "android" / folder / "strings.xml").getroot()
                self.assertEqual({entry.attrib["name"] for entry in resources}, set(keys))

    def test_missing_language_and_unsafe_key(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            del self.strings["greeting"]["es"]
            with self.assertRaises(ValueError):
                generator.generate(self.strings, root, root, root)
            with self.assertRaises(ValueError):
                generator.generate({'../bad': {}}, root, root, root)

    def test_language_subset_writes_only_the_chosen_languages(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["python3", str(ROOT / "implementation/scripts/generate.py"), "--strings", str(ROOT / "tests/fixtures/strings.json"), "--web", str(root / "web"), "--apple", str(root / "apple"), "--android", str(root / "android"), "--languages", "en fr"], check=True)
            self.assertEqual(set(json.loads((root / "web/strings.json").read_text())), {"en", "fr"})
            self.assertEqual(sorted(p.name for p in (root / "android").iterdir()), ["values", "values-fr"])
            catalogue = json.loads((root / "apple/Localizable.xcstrings").read_text())
            self.assertEqual(set(catalogue["strings"]["greeting"]["localizations"]), {"en", "fr"})

    def test_a_chosen_language_must_be_present_and_known(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            del self.strings["greeting"]["de"]
            generator.generate(self.strings, root / "a", root / "b", root / "c", ("en", "fr", "es"))
            with self.assertRaises(ValueError):
                generator.generate(self.strings, root / "d", root / "e", root / "f")
            for bad in ((), ("fr",), ("en", "en"), ("en", "pt")):
                with self.assertRaises(ValueError):
                    generator.generate(self.strings, root / "g", root / "h", root / "i", bad)
            self.assertFalse((root / "g").exists())
        self.assertEqual(generator.parse_languages("en  de"), ("en", "de"))
        for bad in ("", "fr", "en,fr", "en xx"):
            with self.assertRaises(ValueError):
                generator.parse_languages(bad)

    def test_duplicate_keys_rejected(self):
        with self.assertRaises(ValueError):
            json.loads('{"a":1,"a":2}', object_pairs_hook=generator.unique)

    def test_escaping_and_first_appearance(self):
        self.assertEqual(generator.order("{b} {a} {b}"), ["b", "a"])
        self.assertEqual(generator.android("It's \"ready\"\n", []), "It\\'s \\\"ready\\\"\\n")


if __name__ == "__main__":
    unittest.main()
