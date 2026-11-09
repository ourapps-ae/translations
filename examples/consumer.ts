import {selectLanguage, lookup} from "../implementation/web/i18n.ts";

export function greeting(requested: string): string {
  const tables: Record<string, Record<string, string>> = {en: {hello: "Hello"}, fr: {hello: "Bonjour"}};
  return lookup(tables[selectLanguage(requested, Object.keys(tables), "en")], "hello");
}
