export function selectLanguage(requested: string, supported: readonly string[], fallback: string): string {
  if (supported.includes(requested)) return requested;
  const base = requested.split("-")[0];
  return supported.includes(base) ? base : fallback;
}

export function lookup(messages: Record<string, string>, key: string): string {
  return Object.hasOwn(messages, key) ? messages[key] : key;
}

// The `languages` setting is a space-separated list such as "en fr"; every name must be in `known` and none may repeat.
export function parseLanguages(setting: string, known: readonly string[] = ["en", "fr", "de", "es"]): string[] {
  const names = setting.split(/\s+/).filter(Boolean);
  if (names.length === 0 || new Set(names).size !== names.length || names.some((name) => !known.includes(name))) throw new Error("languages must be distinct names from " + known.join(" "));
  return names;
}
