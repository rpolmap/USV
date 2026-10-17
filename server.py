import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = 8000

proc = None
buffer = []
lock = threading.Lock()


def reader(p):
    # Read output character by character so prompts without a newline show up
    while True:
        ch = p.stdout.read(1)
        if not ch:
            break
        with lock:
            buffer.append(ch)


def start():
    global proc
    if proc and proc.poll() is None:
        proc.kill()
    with lock:
        buffer.clear()
    proc = subprocess.Popen(
        [sys.executable, "-u", "web.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    threading.Thread(target=reader, args=(proc,), daemon=True).start()


class Handler(BaseHTTPRequestHandler):
    def reply(self, body, ctype="text/plain; charset=utf-8", extra=None):
        data = body if isinstance(body, bytes) else body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path in ("/", "/python.html"):
            with open("python.html", "rb") as f:
                self.reply(f.read(), "text/html; charset=utf-8")
        elif self.path == "/start":
            start()
            self.reply("ok")
        elif self.path == "/output":
            with lock:
                text = "".join(buffer)
            done = "true" if (proc is None or proc.poll() is not None) else "false"
            self.reply(text, extra={"X-Done": done})
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == "/send":
            n = int(self.headers.get("Content-Length", 0))
            line = self.rfile.read(n).decode("utf-8")
            if proc and proc.poll() is None:
                with lock:
                    buffer.append(line + "\n")  # echo what was typed
                try:
                    proc.stdin.write(line + "\n")
                    proc.stdin.flush()
                except (BrokenPipeError, OSError):
                    pass
            self.reply("ok")
        else:
            self.send_error(404)


if __name__ == "__main__":
    print(f"Open http://localhost:{PORT}")
    ThreadingHTTPServer(("", PORT), Handler).serve_forever()
    
