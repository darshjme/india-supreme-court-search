#!/usr/bin/env python3
"""Tiny static server WITH HTTP Range support (for local sql.js-httpvfs testing).
GitHub Pages already supports ranges; this is only for local dev."""
import http.server, os, re, sys
ROOT=os.path.dirname(os.path.abspath(__file__))

class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self,*a,**k): super().__init__(*a,directory=ROOT,**k)
    def end_headers(self):
        self.send_header("Accept-Ranges","bytes")
        self.send_header("Access-Control-Allow-Origin","*")
        super().end_headers()
    def do_GET(self):
        rng=self.headers.get("Range")
        path=self.translate_path(self.path)
        if not rng or not os.path.isfile(path):
            return super().do_GET()
        m=re.match(r"bytes=(\d+)-(\d*)",rng)
        if not m: return super().do_GET()
        size=os.path.getsize(path)
        start=int(m.group(1)); end=int(m.group(2)) if m.group(2) else size-1
        end=min(end,size-1); length=end-start+1
        ctype=self.guess_type(path)
        self.send_response(206)
        self.send_header("Content-Type",ctype)
        self.send_header("Content-Range",f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length",str(length))
        self.end_headers()
        with open(path,"rb") as f:
            f.seek(start); remaining=length
            while remaining>0:
                chunk=f.read(min(65536,remaining))
                if not chunk: break
                self.wfile.write(chunk); remaining-=len(chunk)
    def log_message(self,*a): pass

if __name__=="__main__":
    port=int(sys.argv[1]) if len(sys.argv)>1 else 8900
    print(f"range server on http://127.0.0.1:{port}  root={ROOT}")
    http.server.ThreadingHTTPServer(("127.0.0.1",port),H).serve_forever()
