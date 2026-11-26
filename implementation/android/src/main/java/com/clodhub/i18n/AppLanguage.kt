package com.clodhub.i18n

fun selectLanguage(requested: String, supported: List<String>, fallback: String): String {
    if (requested in supported) return requested
    val base = requested.substringBefore("-")
    return if (base in supported) base else fallback
}

fun lookup(messages: Map<String, String>, key: String): String = messages[key] ?: key

object AppLanguage {
    fun selectLanguage(requested: String, supported: List<String>, fallback: String): String =
        com.clodhub.i18n.selectLanguage(requested, supported, fallback)
    fun lookup(messages: Map<String, String>, key: String): String = com.clodhub.i18n.lookup(messages, key)
}
