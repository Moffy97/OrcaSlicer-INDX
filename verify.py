"""Repeatable package and protocol checks; no printer connection."""
import hashlib,subprocess,sys
from pathlib import Path,PurePosixPath
root=Path(__file__).resolve().parent
for line in (root/'SHA256SUMS').read_text().splitlines():
 digest,name=line.split('  ',1);path=PurePosixPath(name)
 if path.is_absolute() or '..' in path.parts:raise ValueError('Invalid manifest path')
 if hashlib.sha256(root.joinpath(*path.parts).read_bytes()).hexdigest()!=digest:raise ValueError('Checksum mismatch: '+name)
for script in ('test_profiles.py','test_update.py'):
 subprocess.run([sys.executable,str(root/script)],check=True,cwd=root)
print('Verified package hashes, profile protocol, calibration states, tool counts, commissioning checklist and update/rollback.')
