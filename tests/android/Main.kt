import ae.i18n.selectLanguage
import ae.i18n.lookup
import ae.i18n.AppLanguage

fun main() {
    check(selectLanguage("fr-CA", listOf("en", "fr", "fr-CA"), "en") == "fr-CA")
    check(selectLanguage("fr-CA", listOf("en", "fr"), "en") == "fr")
    check(selectLanguage("", listOf("en", "fr"), "en") == "en")
    check(AppLanguage.selectLanguage("ja", listOf("en", "fr"), "en") == "en")
    check(lookup(mapOf("hello" to "Bonjour"), "hello") == "Bonjour")
    check(lookup(mapOf("hello" to ""), "hello") == "")
    check(AppLanguage.lookup(emptyMap(), "missing") == "missing")
    println("7 language assertions passed")
}
