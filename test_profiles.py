"""Run the archived protocol/generator tests in an isolated temporary workspace."""
from pathlib import Path,PurePosixPath
import tempfile,zipfile,subprocess,sys

with tempfile.TemporaryDirectory() as td,zipfile.ZipFile(Path(__file__).with_name('touchscreen.zip')) as archive:
 root=Path(td)
 for entry in archive.infolist():
  name=PurePosixPath(entry.filename)
  if name.is_absolute() or '..' in name.parts:raise ValueError('Invalid archive path')
  if not entry.filename.endswith('.py'):continue
  if name.parts[0] not in ('touchscreen','tests'):raise ValueError('Unexpected archive entry')
  dest=root.joinpath(*name.parts);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(archive.read(entry))
 for name in ['test-native-protocol.py','test-curated-library.py','test-nozzle-variants.py','test-preflight-profiles.py','test-commissioning.py']:
  subprocess.run([sys.executable,str(root/'tests'/name)],cwd=root,check=True)
print('All isolated profile, hardware-variant and G-code generator tests passed. No printer contacted.')
