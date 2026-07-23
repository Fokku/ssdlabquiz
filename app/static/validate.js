// Frontend check - OWASP Proactive Controls 2024 C7 (Secure Digital Identities),
// Level 1 passwords: at least 12 characters, allow up to 64.
function checkPassword(pw) {
    if (pw.length >= 12 && pw.length <= 64) {
        return true;
    }
    alert("Password must be 12 to 64 characters long");
    return false;
}
