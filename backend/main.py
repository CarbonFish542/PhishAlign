#!/usr/bin/env python3
"""
PhishAlign Backend Entrypoint

Run directly:
    python main.py
Or with uvicorn CLI:
    uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
