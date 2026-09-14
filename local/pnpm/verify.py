#!/usr/bin/env python3
"""Read-only installed-patch and known-host compatibility check."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--profile', required=True, type=Path)
parser.add_argument('--dsh-root', required=True, type=Path)
args = parser.parse_args()
manifest = json.loads(Path(__file__).with_name('manifest.json').read_text())
errors = []
def check_file(path, expected):
    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        errors.append(str(path) + ': absent or hash mismatch')
check_file(args.profile/'patches'/manifest['patch_file'], manifest['patch_sha256'])
package = args.profile/'node_modules'/manifest['package']
for relative, expected in manifest['payload_sha256'].items():
    check_file(package/relative, expected)
profile_manifest = json.loads((args.profile/'package.json').read_text())
if profile_manifest.get('dependencies', {}).get(manifest['package']) != manifest['version']:
    errors.append('package dependency is not pinned to the proved version')
workspace = (args.profile/'pnpm-workspace.yaml').read_text()
if f"{manifest['package']}@{manifest['version']}" not in workspace or manifest['patch_file'] not in workspace:
    errors.append('persistent pnpm patch declaration missing')
head = subprocess.check_output(['git', '-C', str(args.dsh_root), 'rev-parse', 'HEAD'], text=True).strip()
if head != manifest['verified_dsh_commit']:
    errors.append('DSH host changed: native API/browser/tool compatibility must be revalidated')
for error in errors:
    print('FAIL:', error)
if errors:
    raise SystemExit(1)
print('PASS: exact patch, installed payload, version pin, declaration and proved DSH commit')
