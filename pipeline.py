#!/usr/bin/env python3
"""
PhishAlign — Demo Phishing Testbed Pipeline

Dedicated manager for the demo phishing simulation pages (Port 5050).
Backend should be run separately in its own terminal:
    cd backend
    python main.py

Commands:
    python pipeline.py start       -> Starts Demo Phishing Testbed server on http://127.0.0.1:5050
    python pipeline.py open        -> Opens all 3 test phishing scenarios in browser tabs
    python pipeline.py run-tests   -> Runs automated evaluation on all test pages
    python pipeline.py status      -> Checks if demo testbed server is running
    python pipeline.py stop        -> Stops the demo testbed server
    python pipeline.py             -> Interactive menu
"""

from __future__ import annotations

import argparse
import os
import socket
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
DEMO_DIR = ROOT_DIR / "demo-phish"
BACKEND_DIR = ROOT_DIR / "backend"

DEMO_PORT = int(os.environ.get("DEMO_PORT", 5050))
BACKEND_PORT = 8000

TEST_PAGES = [
    {
        "name": "PayPal Credential Harvester",
        "url": f"http://127.0.0.1:{DEMO_PORT}/",
        "file": DEMO_DIR / "index.html",
        "expected_tier": "phishing",
        "expected_brand": "paypal",
    },
    {
        "name": "Microsoft 365 Account Spoof",
        "url": f"http://127.0.0.1:{DEMO_PORT}/microsoft.html",
        "file": DEMO_DIR / "microsoft.html",
        "expected_tier": "phishing",
        "expected_brand": "microsoft",
    },
    {
        "name": "Google Accounts Spoof",
        "url": f"http://127.0.0.1:{DEMO_PORT}/google.html",
        "file": DEMO_DIR / "google.html",
        "expected_tier": "phishing",
        "expected_brand": "google",
    },
]

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def get_pid_on_port(port: int) -> int | None:
    try:
        output = subprocess.check_output(
            "netstat -ano -p tcp", shell=True, text=True, errors="ignore"
        )
        for line in output.strip().splitlines():
            parts = line.split()
            if len(parts) >= 5 and f":{port}" in parts[1] and parts[3].upper() == "LISTENING":
                return int(parts[4])
    except Exception:
        pass
    return None


def is_port_in_use(port: int, host: str = "127.0.0.1") -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            if s.connect_ex((host, port)) == 0:
                return True
    except Exception:
        pass
    return get_pid_on_port(port) is not None


def cmd_status() -> None:
    print("\n" + "=" * 55)
    print("       PhishAlign Demo Pages Testbed Status")
    print("=" * 55)

    demo_ok = is_port_in_use(DEMO_PORT)
    backend_ok = is_port_in_use(BACKEND_PORT)

    d_pid = get_pid_on_port(DEMO_PORT) if demo_ok else None
    d_icon = "[RUNNING]" if demo_ok else "[STOPPED]"
    b_icon = "[ACTIVE]" if backend_ok else "[NOT DETECTED]"

    print(f"  Demo Testbed (Port {DEMO_PORT}):  {d_icon:<11} (PID: {d_pid or '-'})")
    print(f"  Backend API  (Port {BACKEND_PORT}):  {b_icon:<11}")
    if not backend_ok:
        print("  -> Remember to start your backend in another terminal:")
        print("     cd backend && uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload")
    print("=" * 55 + "\n")


def cmd_start() -> None:
    print("\n[*] Starting Demo Phishing Server...")
    if is_port_in_use(DEMO_PORT):
        print(f"  [+] Demo server is already running on http://127.0.0.1:{DEMO_PORT}/")
        cmd_status()
        return

    demo_cmd = [sys.executable, "server.py"]
    if sys.platform == "win32":
        # Launch with dedicated console so handles are valid and logs are visible
        subprocess.Popen(
            demo_cmd,
            cwd=str(DEMO_DIR),
            creationflags=subprocess.CREATE_NEW_CONSOLE,
        )
    else:
        subprocess.Popen(demo_cmd, cwd=str(DEMO_DIR))

    started = False
    for _ in range(15):
        time.sleep(0.3)
        if is_port_in_use(DEMO_PORT):
            started = True
            break

    if started:
        print(f"  [+] Demo testbed running live at http://127.0.0.1:{DEMO_PORT}/")
    else:
        print(f"  [!] Notice: Waiting for port {DEMO_PORT} to accept connections...")
    cmd_status()


def cmd_stop() -> None:
    print("\n[*] Stopping Demo Phishing Server...")
    pid = get_pid_on_port(DEMO_PORT)
    if pid:
        try:
            if sys.platform == "win32":
                subprocess.run(f"taskkill /F /T /PID {pid}", shell=True, check=False, capture_output=True)
            else:
                os.kill(pid, 9)
            print(f"  [+] Stopped Demo Server (PID: {pid}).")
        except Exception as e:
            print(f"  [!] Could not stop Demo Server: {e}")
    else:
        print("  [-] Demo Server is not running.")
    print("Done.\n")


def cmd_open() -> None:
    if not is_port_in_use(DEMO_PORT):
        print("[!] Demo server is not running. Starting it now...")
        cmd_start()

    print("\n[*] Launching test phishing scenarios in browser tabs...")
    for page in TEST_PAGES:
        print(f"  Opening: {page['name']} -> {page['url']}")
        webbrowser.open_new_tab(page["url"])
        time.sleep(0.4)
    print("\n[+] All demo pages launched! Test them with your PhishAlign extension active.\n")


def cmd_run_tests() -> None:
    print("\n" + "=" * 70)
    print("       PhishAlign Demo Pages Evaluation Pipeline")
    print("=" * 70)

    sys.path.insert(0, str(BACKEND_DIR))
    try:
        from app import inference
        import PIL.Image
        import io
    except Exception as e:
        print(f"[!] Could not import backend inference module: {e}")
        return

    dummy_img = PIL.Image.new("RGB", (1280, 900), color=(255, 255, 255))
    buf = io.BytesIO()
    dummy_img.save(buf, format="PNG")
    screenshot_bytes = buf.getvalue()

    passed = 0
    total = len(TEST_PAGES)

    print("\nEvaluating all simulated test scenarios:")
    for page in TEST_PAGES:
        if not page["file"].exists():
            print(f"  [ERROR] Missing file: {page['file']}")
            continue

        html_bytes = page["file"].read_bytes()
        res = inference.analyze_page(
            url=page["url"],
            html_bytes=html_bytes,
            screenshot_bytes=screenshot_bytes,
            page_title=page["name"],
            final_url=page["url"],
        )

        prob = res["phishalign_probability"]
        tier = res["risk_tier"]
        brand = res["intent_signals"].get("impersonated_brand")

        is_pass = tier == page["expected_tier"] and (prob >= 0.78)
        status_icon = "[PASS]" if is_pass else "[FAIL]"
        if is_pass:
            passed += 1

        print(f"  {status_icon:<6} | {page['name']:<28} | Brand: {str(brand):<10} | Prob: {prob*100:5.1f}% | Tier: {tier.upper()}")

    print("\n" + "=" * 70)
    print(f"  Results: {passed}/{total} Scenarios Passed ({(passed/total)*100:.0f}%)")
    print("=" * 70 + "\n")


def interactive_menu() -> None:
    while True:
        print("\n" + "=" * 52)
        print("      PhishAlign Demo Pages Testbed Manager")
        print("=" * 52)
        print("  1. Start Demo Server & Open All Test Pages in Browser")
        print("  2. Open Test Pages in Browser (Server already running)")
        print("  3. Run Automated Evaluation on Demo Pages")
        print("  4. Check Demo Server Status")
        print("  5. Stop Demo Pages Server")
        print("  0. Exit")
        print("=" * 52)
        print("  Note: Run your backend in another terminal:")
        print("    cd backend && python main.py")
        print("=" * 52)

        choice = input("Enter option [0-5]: ").strip()
        if choice == "1":
            cmd_start()
            time.sleep(0.5)
            cmd_open()
        elif choice == "2":
            cmd_open()
        elif choice == "3":
            cmd_run_tests()
        elif choice == "4":
            cmd_status()
        elif choice == "5":
            cmd_stop()
        elif choice in {"0", "exit", "q"}:
            print("Exiting.")
            break
        else:
            print("Invalid choice.")


def main():
    parser = argparse.ArgumentParser(description="PhishAlign Demo Pages Pipeline")
    parser.add_argument(
        "action",
        nargs="?",
        choices=["start", "stop", "open", "run-tests", "status"],
        help="Command to execute",
    )

    args = parser.parse_args()

    if args.action == "start":
        cmd_start()
    elif args.action == "stop":
        cmd_stop()
    elif args.action == "open":
        cmd_open()
    elif args.action == "run-tests":
        cmd_run_tests()
    elif args.action == "status":
        cmd_status()
    else:
        interactive_menu()


if __name__ == "__main__":
    main()
