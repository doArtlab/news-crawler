import re
from html import unescape
import requests

def _strip_scripts_styles(html: str) -> str:
    """Remove <script>, <style>, and HTML comments."""
    html = re.sub(r"(?is)<script[^>]*>.*?</script>", "", html)
    html = re.sub(r"(?is)<style[^>]*>.*?</style>", "", html)
    html = re.sub(r"(?is)<!--.*?-->", "", html)
    return html


def _extract_title(html: str) -> str:
    m = re.search(r"(?is)<title[^>]*>(.*?)</title>", html)
    return unescape(m.group(1).strip()) if m else ""


def _html_to_text(html: str) -> str:
    """Convert HTML to readable plain text without external deps.

    - Drop scripts/styles/comments
    - Insert newlines for common block tags
    - Strip remaining tags
    - Collapse whitespace and empty lines
    """
    html = _strip_scripts_styles(html)
    # Newlines for common block-level tags to preserve structure
    html = re.sub(r"(?is)<\s*(br|p|div|li|tr|td|th|h[1-6])[^>]*>", "\n", html)
    # Remove the rest of tags
    text = re.sub(r"(?is)<[^>]+>", "", html)
    # Unescape HTML entities
    text = unescape(text)
    # Normalize whitespace and drop empty lines
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    return "\n".join(lines)


def scrap_news(url: str) -> str:
    """Fetch the page at `url` and return cleaned text content.

    Returns empty string on failure.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/127.0.0.0 Safari/537.36"
        )
    }
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code != 200:
            print(f"GET {url} -> {resp.status_code}")
            return ""

        # Ensure correct text decoding
        if not resp.encoding:
            try:
                resp.encoding = resp.apparent_encoding or "utf-8"
            except Exception:
                resp.encoding = "utf-8"

        html = resp.text
        title = _extract_title(html)
        body = _html_to_text(html)

        if title and body and not body.startswith(title):
            return f"{title}\n\n{body}"
        return body

    except Exception as e:
        print(f"scrap_news error for {url}: {e}")
        return ""