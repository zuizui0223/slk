"""Pure fixture tests for the real 2025 parentage data provenance probe."""
import hashlib
import io
import json
import sys
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from probe_zenodo_mercu_paternity_v21 import (
    API, archive_inventory, checked_digest, file_entries, probe, safe_source
)

def fixture():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("sample/observations.csv", "dam_id,sire_id,seed_count\nA,B,3\nB,B,4\n")
    raw = buf.getvalue()
    url = "https://zenodo.org/api/records/14542260/files/raw.zip/content"
    metadata = {"id":14542260, "files":[{
        "key":"raw.zip","size":len(raw),"checksum":"md5:"+hashlib.md5(raw).hexdigest(),
        "links":{"self":"https://zenodo.org/api/records/14542260/files/raw.zip", "content":url}
    }]}
    return raw, url, metadata

class ZenodoOriginalParentageProbe(unittest.TestCase):
    def test_urls_and_digest_guard(self):
        raw, url, meta = fixture()
        self.assertTrue(safe_source(url))
        self.assertFalse(safe_source("https://untrusted.example/evil.zip"))
        self.assertFalse(safe_source("http://zenodo.org/insecure.zip"))
        self.assertTrue(checked_digest(raw,meta["files"][0]["checksum"]).startswith("md5:"))
        with self.assertRaises(ValueError):
            checked_digest(raw, "md5:"+"0"*32)
        with self.assertRaises(ValueError):
            checked_digest(raw, "")

    def test_zenodo_file_prefer_content_link(self):
        _, url, meta = fixture()
        rows=file_entries(meta)
        self.assertEqual(rows[0]["url"],url)

    def test_archive_schema_without_extraction(self):
        raw, _, _ = fixture()
        inventory=archive_inventory(raw)
        self.assertEqual(len(inventory),1)
        self.assertEqual(inventory[0]["columns"],["dam_id","sire_id","seed_count"])
        self.assertEqual(inventory[0]["data_rows"],2)

    def test_validated_schema_does_not_claim_new_fitness(self):
        raw, url, meta = fixture()
        def fetch(u):
            if u==API:
                return json.dumps(meta).encode("utf8")
            if u==url:
                return raw
            raise AssertionError("unexpected URL: "+u)
        result=probe(fetch=fetch)
        self.assertEqual(result["state"],"verified_data_schema")
        self.assertTrue(result["downloaded_verified_dataset"])
        self.assertFalse(result["new_fitness_estimates"])

    def test_unavailable_is_visible_not_false_success(self):
        def no_source(_):
            raise TimeoutError("cannot reach data source")
        result=probe(fetch=no_source)
        self.assertEqual(result["state"],"unavailable")
        self.assertFalse(result["downloaded_verified_dataset"])
        self.assertEqual(result["files"],[])
        self.assertIn("TimeoutError",result["error"])

if __name__ == "__main__":
    unittest.main()
