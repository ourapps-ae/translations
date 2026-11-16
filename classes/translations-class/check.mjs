import { assert, load } from './runtime.mjs';
const m = await load('web/index.ts');
assert.equal(m.selectLanguage('fr-CA', ['en', 'fr'], 'en'), 'fr');
assert.equal(m.selectLanguage('unknown', ['en', 'fr'], 'en'), 'en');
assert.equal(m.lookup({ greeting: 'Bonjour' }, 'greeting'), 'Bonjour');
assert.equal(m.lookup({}, 'missing'), 'missing');
assert.deepEqual(m.parseLanguages('fr en'), ['fr', 'en']);
assert.throws(() => m.parseLanguages('fr en fr'));
assert.throws(() => m.parseLanguages('unknown'));
