"""Fixed download fixtures and producer compatibility with the installed consumer."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import hashlib
import os
from pathlib import Path
import sys
import tempfile
from threading import Thread
import unittest
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts/geocsv"))
from create_snapshot import create_snapshot

from mermaid import geocsv


class FetchCompatibility(unittest.TestCase):
    def test_fixed_consumer_baseline_and_historical_manifest(self):
        fixtures = Path(__file__).parent / "fixtures"
        manifest = json.loads((fixtures / "manifest.json").read_bytes())
        payload = (fixtures / "P0006.geocsv").read_bytes()
        self.assertEqual(hashlib.sha256(payload).hexdigest(), manifest["files"][0]["sha256"])
        self.assertEqual(geocsv.read(payload)[0].loc[0, "Station"], "P0006")
        baseline = json.loads((fixtures / "consumer_baseline.json").read_bytes())
        if os.environ.get("MERMAID_CONSUMER_BASELINE") == "1":
            self.assertEqual(geocsv.__version__, baseline["version"])
            sources = Path(geocsv.__file__).parent
            self.assertEqual({p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(sources.glob("*.py"))}, baseline["python_sources"])

    def test_real_client_pins_encoded_timestamp_for_memory_and_disk(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "processed/serial"
            source.mkdir(parents=True)
            # Synthetic data exercises parsing, timestamps and missing values.
            source.joinpath("geo_DET_REQ.csv").write_bytes(
                b"#dataset: GeoCSV\n#created: 2026-10-21T22:48:33.277000001Z\n"
                b"#field_type: string,float\nStation,Latitude\nP0006,-14.4\n")
            inventory = root / "instruments.csv"
            inventory.write_text("instrument_serial,instrument_id\nserial,P0006\n")
            candidate = create_snapshot(source.parent, root / "work", inventory)
            manifest = json.loads((candidate / "manifest.json").read_bytes())
            release = manifest["release_id"]
            prefix = f"/geocsv/releases/{quote(release, safe='')}/"
            responses = {prefix + path.name: path.read_bytes() for path in candidate.iterdir() if path.name != "source_provenance.json"}
            responses["/geocsv/latest.json"] = json.dumps({
                "release_id": release, "testing_only": True,
                "manifest": f"releases/{quote(release, safe='')}/manifest.json"}).encode()
            requests = []
            fixtures = Path(__file__).parent / "fixtures"
            responses["/geocsv/releases/test-001/manifest.json"] = (fixtures / "manifest.json").read_bytes()
            responses["/geocsv/releases/test-001/P0006.geocsv"] = (fixtures / "P0006.geocsv").read_bytes()

            class Handler(BaseHTTPRequestHandler):
                def do_GET(self):
                    requests.append((self.path, self.headers.get("Accept-Encoding")))
                    body = responses.get(self.path)
                    self.send_response(404 if body is None else 200)
                    self.send_header("Content-Length", str(len(body or b"")))
                    self.end_headers()
                    self.wfile.write(body or b"")

                def log_message(self, *args):
                    pass

            server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
            thread = Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                base = f"http://127.0.0.1:{server.server_port}/geocsv/"
                historical = geocsv.fetch(base_url=base, release="test-001", output_dir=None)
                self.assertEqual(historical[0].content, (fixtures / "P0006.geocsv").read_bytes())
                requests.clear()
                results = geocsv.fetch(base_url=base, output_dir=None)
                self.assertEqual(sum(path.endswith("latest.json") for path, _ in requests), 1)
                self.assertEqual(results[0].provenance.release_id, release)
                self.assertEqual(geocsv.read(results)[0].loc[0, "Station"], "P0006")
                requests.clear()
                results = geocsv.fetch("P0006", base_url=base, release=release, output_dir=root / "downloads")
                self.assertFalse(any(path.endswith("latest.json") for path, _ in requests))
                self.assertEqual(results[0].path.parent.name, quote(release, safe=""))
                self.assertEqual(results[0].path.read_bytes(), (candidate / "P0006.geocsv").read_bytes())
                self.assertTrue(all(encoding == "identity" for _, encoding in requests))
            finally:
                server.shutdown()
                server.server_close()
                thread.join()


if __name__ == "__main__":
    unittest.main()
