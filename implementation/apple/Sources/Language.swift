func selectLanguage(_ requested: String, supported: [String], fallback: String) -> String {
    if supported.contains(requested) { return requested }
    let base = String(requested.split(separator: "-", omittingEmptySubsequences: false)[0])
    return supported.contains(base) ? base : fallback
}

func lookup(_ messages: [String: String], key: String) -> String {
    messages[key] ?? key
}
