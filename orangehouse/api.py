"""Minimal JSON API using only the Python standard library."""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse
from .model import Scenario, project

class Handler(BaseHTTPRequestHandler):
    server_version = "OrangeHouse/0.1"
    def _send(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, separators=(",", ":")).encode()
        self.send_response(status)
        for key, value in (("Content-Type", "application/json"), ("Content-Length", str(len(body))),
                           ("X-Content-Type-Options", "nosniff"), ("Cache-Control", "no-store")):
            self.send_header(key, value)
        self.end_headers(); self.wfile.write(body)
    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/health": self._send(200, {"status":"ok","service":"orange-house","version":"0.1.0"})
        elif path == "/ontology": self._send(200, {"entities":["Scenario","Projection","Observation","Control"],"relations":["Scenario produces Projection","Control governs Scenario"]})
        else: self._send(404, {"error":"not_found"})
    def do_POST(self) -> None:
        if urlparse(self.path).path != "/v1/project": self._send(404,{"error":"not_found"}); return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 16384: raise ValueError("body must be between 1 and 16384 bytes")
            data = json.loads(self.rfile.read(length)); allowed={"starting_value","monthly_flow","annual_rate","volatility","months"}
            unknown=set(data)-allowed
            if unknown: raise ValueError(f"unknown fields: {', '.join(sorted(unknown))}")
            self._send(200, project(Scenario(**data)))
        except (ValueError, TypeError, json.JSONDecodeError) as exc: self._send(400,{"error":"invalid_request","detail":str(exc)})
    def log_message(self, fmt: str, *args) -> None: print(json.dumps({"event":"http_request","message":fmt % args}))

def serve(host="127.0.0.1", port=8080):
    print(f"Orange House listening on http://{host}:{port}")
    ThreadingHTTPServer((host, port), Handler).serve_forever()
