# Local workflow

Local only: no commits, pushes, remote changes or publishing without George's say-so. Licence wording remains deferred.

Commands from the package root: `node --test tests/web.test.ts`, `python3 -m unittest discover -s tests -p 'test_*.py'`, `python3 tests/native.py apple`, `python3 tests/native.py android` (kotlinc is not installed here, so the Android check does not run).
Generator: `python3 implementation/scripts/generate.py --strings FILE --web DIR --apple DIR --android DIR`.
Review a fetched archive: `python3 -m aepm review <digest> --store STORE --policy POLICY --trusted --allow-network`. Always `-B`.
