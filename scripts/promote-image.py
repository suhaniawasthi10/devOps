#!/usr/bin/env python3
"""Update the desired image; does not commit or push automatically."""
import argparse
from pathlib import Path
import re

parser = argparse.ArgumentParser()
parser.add_argument("sha", help="Full 40-character commit SHA from a successful publishing run")
args = parser.parse_args()
if not re.fullmatch(r"[0-9a-f]{40}", args.sha):
    parser.error("use a full lowercase commit SHA")
p = Path(__file__).resolve().parents[1] / "final-devops-project/gitops/values.yaml"
s = p.read_text()
s = re.sub(r"  repository: .+", "  repository: ghcr.io/suhaniawasthi10/devops/notes", s)
s = re.sub(r"  tag: .+", '  tag: "' + args.sha + '"', s)
p.write_text(s)
print("Updated", p, "— review, commit and push to promote this tested image.")
