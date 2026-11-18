#!/usr/bin/env python3
"""Read-only provenance and schema probe for Chen & Pannell (2025) raw parentage data.

Downloads a public Zenodo record in CI; does not execute archived scripts,
extract archives, fit a model or infer fitness. A failed fetch is explicitly
reported as unavailable, not counted as successful data acquisition.
"""
import argparse
import csv
import hashlib
import io
import json
import urllib.request
import zipfile
from pathlib import Path
from urllib.parse import urlsplit

RECORD_ID = 14542260
DOI = "10.5281/zenodo.14542260"
API = f"https://zenodo.org/api/records/{RECORD_ID}"
MAX_DOWNLOAD = 30 * 1024 * 1024

def file_entries(metadata):
    files = metadata.get("files", [])
    if isinstance(files, dict):
        files = files.get("entries", files)
        if isinstance(files, dict):
            files = list(files.values())
    if not isinstance(files, list):
        raise ValueError("Unexpected Zenodo files schema")
    return [{
        "name": f.get("key", f.get("filename", "")),
        "size": f.get("size", 0),
        "checksum": f.get("checksum", f.get("md5", "")),
        "url": f.get("links", {}).get("self", f.get("links", {}).get("content"))
    } for f in files]

def safe_source(url):
    parsed = urlsplit(url or "")
    return parsed.scheme == "https" and parsed.hostname in {"zenodo.org", "www.zenodo.org"}

def checked_digest(raw, checksum):
    if not checksum:
        raise ValueError("No published checksum; cannot verify raw data")
    if ":" in checksum:
        algorithm, expected = checksum.split(":", 1)
    else:
        algorithm, expected = "md5", checksum
    if algorithm not in {"md5", "sha256"}:
        raise ValueError("Unsupported checksum algorithm")
    result = getattr(hashlib, algorithm)(raw).hexdigest()
    if result.lower() != expected.lower():
        raise ValueError("Published checksum mismatch")
    return algorithm + ":" + result

def archive_inventory(raw):
    if not zipfile.is_zipfile(io.BytesIO(raw)):
        return []
    found = []
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        for f in z.infolist():
            if f.is_dir():
                continue
            item = {"entry": f.filename, "uncompressed_bytes": f.file_size}
            if f.file_size <= 2_000_000 and f.filename.lower().endswith((".csv", ".tsv")):
                try:
                    lines = z.read(f).decode("utf-8-sig").splitlines()
                    dialect = "excel-tab" if f.filename.lower().endswith(".tsv") else "excel"
                    rows = csv.reader(lines, dialect=dialect)
                    first = next(rows, [])
                    item["columns"] = first[:100]
                    item["data_rows"] = max(len(lines)-1, 0)
                except (UnicodeError, csv.Error, OSError, RuntimeError) as exc:
                    item["schema_error"] = type(exc).__name__
            found.append(item)
    return found

def open_url(url, max_bytes=MAX_DOWNLOAD):
    if not safe_source(url):
        raise ValueError("Source URL outside Zenodo HTTPS")
    request = urllib.request.Request(url, headers={
        "User-Agent": "SLK-research-source-audit/1.0",
        "Accept": "application/json, application/octet-stream"
    })
    with urllib.request.urlopen(request, timeout=35) as r:
        data = r.read(max_bytes + 1)
    if len(data) > max_bytes:
        raise ValueError("Download exceeds size limit")
    return data

def probe(fetch=open_url):
    out = {
        "schema": "SLK_2025_REAL_PARENTAGE_SOURCE_ACCESS_PROBE_V21",
        "paper_doi": "10.1111/nph.70356",
        "zenodo_doi": DOI,
        "zenodo_api": API,
        "state": "unavailable",
        "downloaded_verified_dataset": False,
        "new_fitness_estimates": False,
        "files": [],
        "limitations": [
            "An archive checksum only verifies bytes, not the scientific interpretation.",
            "Raw parental and offspring genotypes must be joined with validated keys.",
            "Observed seed paternity and hypothetical inbreeding depression are distinct.",
            "No new model or natural inbreeding-depression estimate was fitted."
        ]
    }
    try:
        meta = json.loads(fetch(API).decode("utf8"))
        if str(meta.get("id")) != str(RECORD_ID):
            raise ValueError("Unexpected record ID")
        items = file_entries(meta)
        if not items:
            raise ValueError("No files in published source record")
        out["state"] = "record_metadata_verified"
        for file in items:
            item = {
                "name":file["name"], "published_size":file["size"],
                "published_checksum":file["checksum"], "status":"not_downloaded"
            }
            if (file["url"] and safe_source(file["url"])
                    and file["name"].lower().endswith((".zip",".csv",".tsv"))
                    and file["size"] <= MAX_DOWNLOAD):
                try:
                    raw = fetch(file["url"])
                    item["verified_digest"] = checked_digest(raw, file["checksum"])
                    item["status"] = "verified"
                    if file["name"].lower().endswith(".zip"):
                        item["archive_entries"] = archive_inventory(raw)
                    else:
                        data = raw.decode("utf-8-sig")
                        rows = list(csv.reader(io.StringIO(data), dialect="excel-tab" if file["name"].lower().endswith(".tsv") else "excel"))
                        item["columns"] = (rows[0] if rows else [])[:100]
                        item["data_rows"] = max(len(rows)-1, 0)
                except Exception as exc:
                    item["status"] = "download_failed"
                    item["error"] = type(exc).__name__ + ": " + str(exc)[:160]
            out["files"].append(item)
        out["downloaded_verified_dataset"] = any(x["status"]=="verified" for x in out["files"])
        out["state"] = "verified_data_schema" if out["downloaded_verified_dataset"] else "metadata_only"
    except Exception as exc:
        out["error"] = type(exc).__name__ + ": " + str(exc)[:200]
    return out

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    value = probe()
    Path(args.out).write_text(json.dumps(value,indent=2,ensure_ascii=False)+"\n", encoding="utf8")
    print(json.dumps(value, indent=2, ensure_ascii=False))
    print("SLK_V21_SOURCE_PROBE_" + value["state"].upper())

if __name__=="__main__":
    main()
