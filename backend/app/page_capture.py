from __future__ import annotations

import ipaddress
import socket
from dataclasses import dataclass
from functools import lru_cache
from urllib.parse import urlparse

from playwright.sync_api import (
    Browser,
    BrowserContext,
    Download,
    Page,
    Request,
    Route,
    sync_playwright,
)

NAVIGATION_TIMEOUT_MS = 20_000
MAX_REDIRECTS = 10

BOT_WALL_TITLES = {
    "just a moment...",
    "attention required!",
    "access denied",
    "please wait...",
    "security check",
    "ddos-guard",
    "enable javascript and cookies to continue",
}


@dataclass
class CaptureResult:
    requested_url: str
    final_url: str
    html: bytes
    screenshot: bytes
    title: str
    status_code: int | None


@lru_cache(maxsize=512)
def _is_public_hostname(hostname: str) -> bool:
    if not hostname:
        return False

    hostname = hostname.rstrip(".").lower()

    blocked_names = {
        "localhost",
        "localhost.localdomain",
        "ip6-localhost",
        "ip6-loopback",
    }

    if hostname in blocked_names or hostname.endswith(".localhost"):
        return False

    try:
        addresses = socket.getaddrinfo(
            hostname,
            None,
            type=socket.SOCK_STREAM,
        )
    except socket.gaierror:
        return False

    if not addresses:
        return False

    for address in addresses:
        ip_text = address[4][0]

        try:
            ip = ipaddress.ip_address(ip_text)
        except ValueError:
            return False

        if (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_reserved
            or ip.is_multicast
            or ip.is_unspecified
        ):
            return False

    return True


def validate_url(url: str) -> str:
    if not isinstance(url, str):
        raise ValueError("URL must be a string.")

    url = url.strip()

    if not url:
        raise ValueError("URL is empty.")

    parsed = urlparse(url)

    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Only HTTP and HTTPS URLs are allowed.")

    if not parsed.hostname:
        raise ValueError("URL does not contain a valid hostname.")

    if parsed.username is not None or parsed.password is not None:
        raise ValueError(
            "URLs containing embedded credentials are not allowed."
        )

    # Allow ports 5050, 5055 as dedicated local demo phishing testbed
    is_demo_testbed = parsed.port in {5050, 5055, 8055} and parsed.hostname in {"localhost", "127.0.0.1"}

    if not is_demo_testbed and not _is_public_hostname(parsed.hostname):
        raise ValueError(
            "The target host is not publicly reachable."
        )

    return url


def _cancel_download(download: Download) -> None:
    try:
        download.cancel()
    except Exception:
        pass


def capture_url(url: str) -> CaptureResult:
    validated_url = validate_url(url)

    security_error: str | None = None
    redirect_limit_error: str | None = None

    with sync_playwright() as playwright:
        browser: Browser = playwright.chromium.launch(
            headless=True,
            downloads_path=None,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ],
        )

        context: BrowserContext = browser.new_context(
            viewport={"width": 1280, "height": 900},
            java_script_enabled=True,
            accept_downloads=False,
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/129.0.0.0 Safari/537.36"
            ),
            locale="en-US",
            timezone_id="America/New_York",
            extra_http_headers={
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "Upgrade-Insecure-Requests": "1",
            },
        )

        page: Page = context.new_page()

        # Layer 2: Hide automation fingerprints that Cloudflare detects
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
            Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
            window.chrome = { runtime: {} };
        """)

        page.set_default_navigation_timeout(NAVIGATION_TIMEOUT_MS)
        page.set_default_timeout(NAVIGATION_TIMEOUT_MS)

        def handle_route(route: Route, request: Request) -> None:
            nonlocal security_error
            nonlocal redirect_limit_error

            request_url = request.url
            is_top_level_nav = (
                request.is_navigation_request() and request.frame == page.main_frame
            )

            # Allow inline data/blob subresources
            parsed_scheme = urlparse(request_url).scheme.lower()
            if not is_top_level_nav and parsed_scheme in {"data", "blob"}:
                route.continue_()
                return

            try:
                validate_url(request_url)
            except ValueError as exc:
                # Only fail the entire capture if the main document navigation is unsafe.
                # Broken/private 3rd-party subresources are simply aborted.
                if is_top_level_nav and security_error is None:
                    security_error = f"Blocked unsafe navigation request: {request_url} ({exc})"
                route.abort()
                return

            if is_top_level_nav:
                redirect_count = 0
                previous = request.redirected_from

                while previous is not None:
                    redirect_count += 1
                    previous = previous.redirected_from

                if redirect_count > MAX_REDIRECTS:
                    redirect_limit_error = f"Maximum redirect limit exceeded: {MAX_REDIRECTS}"
                    route.abort()
                    return

            route.continue_()

        context.route("**/*", handle_route)
        page.on("download", _cancel_download)

        try:
            try:
                response = page.goto(
                    validated_url,
                    wait_until="domcontentloaded",
                    timeout=NAVIGATION_TIMEOUT_MS,
                )
            except Exception as exc:
                if security_error is not None:
                    raise RuntimeError(security_error) from None
                if redirect_limit_error is not None:
                    raise RuntimeError(redirect_limit_error) from None
                raise RuntimeError(f"Page capture failed: {exc}") from None

            final_url = page.url

            try:
                validate_url(final_url)
            except ValueError as exc:
                raise RuntimeError(
                    f"Unsafe final URL blocked: {final_url} ({exc})"
                ) from None

            if security_error is not None:
                raise RuntimeError(security_error)

            if redirect_limit_error is not None:
                raise RuntimeError(redirect_limit_error)

            page.wait_for_timeout(1500)

            html_bytes = page.content().encode("utf-8")
            screenshot = page.screenshot(type="png", full_page=True)
            title = page.title()
            status_code = response.status if response is not None else None

            # Layer 3: Bot-challenge / Cloudflare guardrail
            if title.lower().strip() in BOT_WALL_TITLES or (
                status_code in (403, 429, 503)
                and ("challenge" in final_url.lower() or "__cf_chl" in final_url.lower())
            ):
                raise RuntimeError(
                    f"Bot-protection wall detected (title: '{title}', HTTP {status_code}). "
                    "The website blocked automated access. This page cannot be analysed by PhishAlign."
                )

            return CaptureResult(
                requested_url=validated_url,
                final_url=final_url,
                html=html_bytes,
                screenshot=screenshot,
                title=title,
                status_code=status_code,
            )

        finally:
            context.close()
            browser.close()