# Local workflow

Local only: no commits, pushes, remote changes or publishing without George's say-so. Licence wording remains deferred.
Do not edit `mcinpoker/`, `skull/`, `aepm/`, `OurPoker/proof/` or `OurPoker/recipe/`.

Commands from the package root: `node --test tests/web.test.ts`, `python3 -m unittest discover -s tests -p 'test_*.py'`, `python3 tests/native.py apple`, `python3 tests/native.py android` (kotlinc is not installed here, so the Android check does not run).
Generator: `python3 implementation/scripts/generate.py --strings FILE --web DIR --apple DIR --android DIR`.
Validate: `PYTHONPATH=/Users/george/Projects/com/my/aepm /Users/george/.pyenv/versions/3.12.8/bin/python3.12 -B /Users/george/Projects/com/my/tools/check_component.py components/translations`. Always `-B`.
