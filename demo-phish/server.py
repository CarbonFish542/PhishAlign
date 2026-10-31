import http.server
import os
import socketserver
import sys

PORT = int(os.environ.get("DEMO_PORT", 5050))
DIRECTORY = os.path.dirname(os.path.abspath(__file__))


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        try:
            sys.stderr.write("%s - - [%s] %s\n" %
                             (self.address_string(),
                              self.log_date_time_string(),
                              format % args))
            sys.stderr.flush()
        except Exception:
            pass


if __name__ == "__main__":
    print("=" * 60, flush=True)
    print(f"[*] PhishAlign Demo Phishing Testbed Server", flush=True)
    print(f"[*] Serving files from: {DIRECTORY}", flush=True)
    print(f"[*] URL: http://127.0.0.1:{PORT}/", flush=True)
    print("    Press CTRL+C in this window to stop the server.", flush=True)
    print("=" * 60, flush=True)

    try:
        with ReusableTCPServer(("127.0.0.1", PORT), Handler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Demo phishing server stopped.")
    except Exception as e:
        print(f"[!] Server error: {e}", file=sys.stderr, flush=True)
