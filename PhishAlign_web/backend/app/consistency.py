import re
from urllib.parse import urlsplit

import tldextract


# ============================================================
# FINAL PhishAlign CONSISTENCY FEATURES
# ============================================================

CONSISTENCY_FEATURES = [
    "html_available",
    "ocr_available",
    "title_available",
    "both_html_ocr_available",
    "url_host_available",

    "url_html_jaccard",
    "url_html_containment",
    "url_ocr_jaccard",
    "url_ocr_containment",
    "url_title_jaccard",
    "url_title_containment",
    "html_ocr_jaccard",
    "html_ocr_containment",
    "title_ocr_jaccard",
    "title_ocr_containment",

    "domain_identity_token_count_v3",
    "domain_html_jaccard_v3",
    "domain_html_containment_v3",
    "domain_html_comparison_available_v3",
    "domain_ocr_jaccard_v3",
    "domain_ocr_containment_v3",
    "domain_ocr_comparison_available_v3",
    "domain_title_jaccard_v3",
    "domain_title_containment_v3",
    "domain_title_comparison_available_v3",
]


# ============================================================
# Tokenization — EXACT v1 LOGIC
# ============================================================

def clean_text(value):
    if value is None:
        return ""

    return str(value).strip()


def tokenize(text):
    """
    Same tokenization used by the original v1 extractor.

    Keeps alphanumeric Unicode tokens of at least 2 characters.
    """
    if not text:
        return set()

    return {
        token
        for token in re.findall(
            r"[^\W_]+",
            str(text).lower(),
            flags=re.UNICODE,
        )
        if len(token) >= 2
    }


# ============================================================
# URL hostname — EXACT v1 LOGIC
# ============================================================

def extract_host_tokens(raw_url):
    """
    Extract meaningful hostname tokens.

    Generic hostname parts such as www, com, net, org
    are excluded.
    """

    if raw_url is None:
        return set(), ""

    value = str(raw_url).strip()

    if not value:
        return set(), ""

    try:
        parsed = urlsplit(
            value if "://" in value else "http://" + value
        )
        hostname = parsed.hostname or ""
    except Exception:
        hostname = ""

    hostname = hostname.lower().strip(".")

    if not hostname:
        return set(), ""

    try:
        hostname = hostname.encode("idna").decode("ascii")
    except Exception:
        pass

    if hostname.startswith("www."):
        hostname = hostname[4:]

    generic_parts = {
        "www",
        "com",
        "net",
        "org",
        "edu",
        "gov",
        "co",
        "in",
        "uk",
        "us",
        "de",
        "fr",
        "io",
        "info",
        "biz",
        "online",
        "site",
        "xyz",
        "top",
        "app",
    }

    parts = set(re.findall(r"[a-z0-9]+", hostname))

    meaningful = {
        part
        for part in parts
        if part not in generic_parts and len(part) >= 2
    }

    return meaningful, hostname


# ============================================================
# v1 similarity
# ============================================================

def similarity_features(
    left_tokens,
    right_tokens,
    left_available,
    right_available,
):
    """
    Exact v1 behavior.

    Jaccard:
        intersection / union

    Containment:
        intersection / size of smaller set

    If either side is unavailable, both values are zero.
    """

    if not left_available or not right_available:
        return 0.0, 0.0

    if not left_tokens or not right_tokens:
        return 0.0, 0.0

    intersection = len(left_tokens & right_tokens)
    union = len(left_tokens | right_tokens)
    smaller = min(len(left_tokens), len(right_tokens))

    jaccard = intersection / union if union else 0.0
    containment = intersection / smaller if smaller else 0.0

    return jaccard, containment


# ============================================================
# v3 DOMAIN IDENTITY LOGIC
# ============================================================

# This matches the v3 extractor configuration.
extractor = tldextract.TLDExtract(
    suffix_list_urls=()
)


def get_hostname(url):
    """
    v3 hostname extraction.
    """

    if url is None:
        return ""

    value = str(url).strip()

    if not value:
        return ""

    candidate = (
        value
        if "://" in value
        else "//" + value
    )

    try:
        hostname = urlsplit(candidate).hostname
    except Exception:
        hostname = None

    if not hostname:
        return ""

    return hostname.lower().strip(".")


def get_domain_parts(hostname):
    """
    Return:

        registrable_domain
        core_label
        suffix_known
    """

    if not hostname:
        return "", "", False

    result = extractor(hostname)

    if not result.domain or not result.suffix:
        return "", result.domain or "", False

    registrable_domain = (
        f"{result.domain}.{result.suffix}"
    )

    core_label = result.domain

    return (
        registrable_domain,
        core_label,
        True,
    )


def identity_tokens(core_label):
    """
    v3 domain identity tokenization.

    Only alphabetic sequences of at least 3
    characters are retained.
    """

    return set(
        re.findall(
            r"[a-z]{3,}",
            clean_text(core_label).lower(),
        )
    )


def text_tokens(text):
    """
    v3 comparison tokenization.
    """

    return set(
        re.findall(
            r"[a-z]{3,}",
            clean_text(text).lower(),
        )
    )


def compare_identity_to_text(
    domain_tokens,
    text,
):
    """
    Compare domain identity tokens against
    extracted HTML/OCR/title text.

    Returns:

        jaccard
        containment
        occurrence
        comparison_available
    """

    text_set = text_tokens(text)

    available = (
        bool(domain_tokens)
        and bool(text_set)
    )

    if not available:
        return (
            0.0,
            0.0,
            0,
            int(
                bool(domain_tokens)
                and bool(text)
            ),
        )

    intersection = len(
        domain_tokens & text_set
    )

    union = len(
        domain_tokens | text_set
    )

    jaccard = (
        intersection / union
        if union
        else 0.0
    )

    containment = (
        intersection / len(domain_tokens)
        if domain_tokens
        else 0.0
    )

    occurrence = int(
        bool(intersection)
    )

    return (
        jaccard,
        containment,
        occurrence,
        1,
    )


# ============================================================
# MAIN FEATURE EXTRACTION
# ============================================================

def extract_consistency_features(
    url: str,
    html_text: str = "",
    html_title: str = "",
    ocr_text: str = "",
):
    """
    Extract the exact 25 PhishAlign consistency features.

    Parameters
    ----------
    url:
        Original webpage URL.

    html_text:
        Visible/static text extracted from HTML.

    html_title:
        HTML <title> text.

    ocr_text:
        OCR text extracted from the screenshot.

    Returns
    -------
    dict
        Exactly 25 model features in CONSISTENCY_FEATURES order.
    """

    html_text = clean_text(html_text)
    ocr_text = clean_text(ocr_text)
    html_title = clean_text(html_title)

    # --------------------------------------------------------
    # Availability
    # --------------------------------------------------------

    html_available = bool(html_text)
    ocr_available = bool(ocr_text)
    title_available = bool(html_title)

    # --------------------------------------------------------
    # v1 tokens
    # --------------------------------------------------------

    html_tokens = tokenize(html_text)
    ocr_tokens = tokenize(ocr_text)
    title_tokens = tokenize(html_title)

    host_tokens, hostname = extract_host_tokens(url)

    # --------------------------------------------------------
    # URL ↔ HTML
    # --------------------------------------------------------

    url_html_jaccard, url_html_containment = (
        similarity_features(
            host_tokens,
            html_tokens,
            bool(host_tokens),
            html_available,
        )
    )

    # --------------------------------------------------------
    # URL ↔ OCR
    # --------------------------------------------------------

    url_ocr_jaccard, url_ocr_containment = (
        similarity_features(
            host_tokens,
            ocr_tokens,
            bool(host_tokens),
            ocr_available,
        )
    )

    # --------------------------------------------------------
    # URL ↔ title
    # --------------------------------------------------------

    url_title_jaccard, url_title_containment = (
        similarity_features(
            host_tokens,
            title_tokens,
            bool(host_tokens),
            title_available,
        )
    )

    # --------------------------------------------------------
    # HTML ↔ OCR
    # --------------------------------------------------------

    html_ocr_jaccard, html_ocr_containment = (
        similarity_features(
            html_tokens,
            ocr_tokens,
            html_available,
            ocr_available,
        )
    )

    # --------------------------------------------------------
    # Title ↔ OCR
    # --------------------------------------------------------

    title_ocr_jaccard, title_ocr_containment = (
        similarity_features(
            title_tokens,
            ocr_tokens,
            title_available,
            ocr_available,
        )
    )

    # ========================================================
    # v3 DOMAIN IDENTITY
    # ========================================================

    domain_hostname = get_hostname(url)

    registrable_domain, core_label, suffix_known = (
        get_domain_parts(domain_hostname)
    )

    domain_tokens = identity_tokens(core_label)

    (
        domain_html_jaccard,
        domain_html_containment,
        _domain_html_occurrence,
        domain_html_available,
    ) = compare_identity_to_text(
        domain_tokens,
        html_text,
    )

    (
        domain_ocr_jaccard,
        domain_ocr_containment,
        _domain_ocr_occurrence,
        domain_ocr_available,
    ) = compare_identity_to_text(
        domain_tokens,
        ocr_text,
    )

    (
        domain_title_jaccard,
        domain_title_containment,
        _domain_title_occurrence,
        domain_title_available,
    ) = compare_identity_to_text(
        domain_tokens,
        html_title,
    )

    # ========================================================
    # FINAL 25 FEATURES
    # ========================================================

    features = {
        # Availability
        "html_available": int(html_available),
        "ocr_available": int(ocr_available),
        "title_available": int(title_available),
        "both_html_ocr_available": int(
            html_available and ocr_available
        ),
        "url_host_available": int(
            bool(host_tokens)
        ),

        # URL ↔ HTML
        "url_html_jaccard": url_html_jaccard,
        "url_html_containment": url_html_containment,

        # URL ↔ OCR
        "url_ocr_jaccard": url_ocr_jaccard,
        "url_ocr_containment": url_ocr_containment,

        # URL ↔ title
        "url_title_jaccard": url_title_jaccard,
        "url_title_containment": url_title_containment,

        # HTML ↔ OCR
        "html_ocr_jaccard": html_ocr_jaccard,
        "html_ocr_containment": html_ocr_containment,

        # title ↔ OCR
        "title_ocr_jaccard": title_ocr_jaccard,
        "title_ocr_containment": title_ocr_containment,

        # Domain identity
        "domain_identity_token_count_v3": len(
            domain_tokens
        ),

        "domain_html_jaccard_v3":
            domain_html_jaccard,

        "domain_html_containment_v3":
            domain_html_containment,

        "domain_html_comparison_available_v3":
            domain_html_available,

        "domain_ocr_jaccard_v3":
            domain_ocr_jaccard,

        "domain_ocr_containment_v3":
            domain_ocr_containment,

        "domain_ocr_comparison_available_v3":
            domain_ocr_available,

        "domain_title_jaccard_v3":
            domain_title_jaccard,

        "domain_title_containment_v3":
            domain_title_containment,

        "domain_title_comparison_available_v3":
            domain_title_available,
    }

    # --------------------------------------------------------
    # Safety check
    # --------------------------------------------------------

    if list(features.keys()) != CONSISTENCY_FEATURES:
        raise RuntimeError(
            "Consistency feature order does not match "
            "the frozen PhishAlign feature definition."
        )

    return features


def consistency_vector(
    url: str,
    html_text: str = "",
    html_title: str = "",
    ocr_text: str = "",
):
    """
    Return the 25 features as a list in the exact
    order expected by the PhishAlign stacker.
    """

    features = extract_consistency_features(
        url=url,
        html_text=html_text,
        html_title=html_title,
        ocr_text=ocr_text,
    )

    return [
        features[name]
        for name in CONSISTENCY_FEATURES
    ]