from __future__ import annotations

import ipaddress
import socket
from dataclasses import dataclass
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


@dataclass
class CaptureResult:
    requested_url: str
    final_url: str
    html: bytes
    screenshot: bytes
    title: str
    status_code: int | None


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

    if not _is_public_hostname(parsed.hostname):
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
        )

        context: BrowserContext = browser.new_context(
            viewport={
                "width": 1280,
                "height": 900,
            },
            java_script_enabled=True,
            accept_downloads=False,
        )

        page: Page = context.new_page()

        page.set_default_navigation_timeout(
            NAVIGATION_TIMEOUT_MS
        )
        page.set_default_timeout(
            NAVIGATION_TIMEOUT_MS
        )

        def inspect_request(request: Request) -> None:
            nonlocal security_error
            nonlocal redirect_limit_error

            request_url = request.url

            try:
                validate_url(request_url)
            except ValueError as exc:
                if security_error is None:
                    security_error = (
                        f"Blocked unsafe request: "
                        f"{request_url} ({exc})"
                    )
                return

            if request.is_navigation_request():
                redirect_count = 0
                previous = request.redirected_from

                while previous is not None:
                    redirect_count += 1
                    previous = previous.redirected_from

                if redirect_count > MAX_REDIRECTS:
                    redirect_limit_error = (
                        f"Maximum redirect limit exceeded: "
                        f"{MAX_REDIRECTS}"
                    )

        def handle_route(
            route: Route,
            request: Request,
        ) -> None:
            nonlocal security_error
            nonlocal redirect_limit_error

            request_url = request.url

            try:
                validate_url(request_url)
            except ValueError as exc:
                if security_error is None:
                    security_error = (
                        f"Blocked unsafe request: "
                        f"{request_url} ({exc})"
                    )

                route.abort()
                return

            if request.is_navigation_request():
                redirect_count = 0
                previous = request.redirected_from

                while previous is not None:
                    redirect_count += 1
                    previous = previous.redirected_from

                if redirect_count > MAX_REDIRECTS:
                    redirect_limit_error = (
                        f"Maximum redirect limit exceeded: "
                        f"{MAX_REDIRECTS}"
                    )

                    route.abort()
                    return

            route.continue_()

        # Observe every request. This gives us a reliable record of
        # the reason when Chromium reports a generic navigation error.
        page.on(
            "request",
            inspect_request,
        )

        # Actually enforce the policy.
        context.route(
            "**/*",
            handle_route,
        )

        page.on(
            "download",
            _cancel_download,
        )

        try:
            try:
                response = page.goto(
                    validated_url,
                    wait_until="domcontentloaded",
                    timeout=NAVIGATION_TIMEOUT_MS,
                )

            except Exception as exc:
                if security_error is not None:
                    raise RuntimeError(
                        security_error
                    ) from None

                if redirect_limit_error is not None:
                    raise RuntimeError(
                        redirect_limit_error
                    ) from None

                raise RuntimeError(
                    f"Page capture failed: {exc}"
                ) from None

            final_url = page.url

            try:
                validate_url(final_url)
            except ValueError as exc:
                raise RuntimeError(
                    f"Unsafe final URL blocked: "
                    f"{final_url} ({exc})"
                ) from None

            if security_error is not None:
                raise RuntimeError(
                    security_error
                )

            if redirect_limit_error is not None:
                raise RuntimeError(
                    redirect_limit_error
                )

            page.wait_for_timeout(1000)

            html_bytes = page.content().encode("utf-8")

            screenshot = page.screenshot(
                type="png",
                full_page=True,
            )

            title = page.title()

            status_code = (
                response.status
                if response is not None
                else None
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