"""Download NSL-KDD from the frozen mirror commit and verify SHA-256.

Usage: python scripts/fetch_nsl_kdd.py [target_dir]   (default: data/)
"""
import hashlib
import sys
import urllib.request
from pathlib import Path

MIRROR_COMMIT = "27bbbdf5c5cccf9970b8b6037a0f19dc09c5a0a9"
BASE = f"https://raw.githubusercontent.com/Jehuty4949/NSL_KDD/{MIRROR_COMMIT}/"
FILES = {
    "KDDTrain+.txt": ("1b86d2f957b33082081bba410fe129b475efebcc13c9014c3f447c8271aadf95", 125973),
    "KDDTest+.txt": ("fa46b0935342616aa83b7c2578db355b6a7aaabbc492248172c7a1e8b7ab8f84", 22544),
}


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main(target):
    target = Path(target)
    target.mkdir(parents=True, exist_ok=True)
    for name, (expected, rows) in FILES.items():
        path = target / name
        if not path.exists():
            print("Downloading", name)
            urllib.request.urlretrieve(BASE + name, path)
        actual = sha256(path)
        if actual != expected:
            raise SystemExit(f"SHA-256 mismatch for {name}: {actual}")
        with open(path, "rb") as stream:
            count = sum(1 for _ in stream)
        if count != rows:
            raise SystemExit(f"Row count mismatch for {name}: {count} != {rows}")
        print(f"OK {name}  sha256={actual}  rows={count}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "data")
