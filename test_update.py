"""Exercise install, repeat update and rollback using only temporary directories."""
import json,subprocess,sys,tempfile
from pathlib import Path
installer=Path(__file__).with_name('install_klipperscreen.py')
subprocess.run([sys.executable,str(installer),'--check'],check=True)
with tempfile.TemporaryDirectory() as td:
 root=Path(td);ks=root/'screen';config=root/'config';(ks/'panels').mkdir(parents=True);(ks/'ks_includes').mkdir();config.mkdir()
 old='# original panel\n';(ks/'panels/indx_profiles.py').write_text(old)
 original='[main]\n';(config/'KlipperScreen.conf').write_text(original)
 data=config/'indx-filament-library.json';data.write_text('{"profiles":{}}')
 command=[sys.executable,str(installer),'--klipperscreen-dir',str(ks),'--config-dir',str(config)]
 subprocess.run(command,check=True);backups=sorted(config.glob('indx-screen-backup-*'));first=backups[0]
 assert (ks/'panels/indx_setup.py').is_file()
 assert json.loads((config/'indx-installed-version.json').read_text())['version']=='0.3.0-preview'
 assert (ks/'panels/indx_machine_panel.py').is_file()
 subprocess.run(command,check=True)
 assert (config/'KlipperScreen.conf').read_text().count('[menu __main indx setup]')==1
 # User calibrations made after an update must survive a software rollback.
 data.write_text('{"profiles":{"new":"keep me"}}')
 subprocess.run(command+['--rollback',str(first)],check=True)
 assert (ks/'panels/indx_profiles.py').read_text()==old
 assert not (ks/'panels/indx_setup.py').exists()
 assert not (ks/'panels/indx_machine_panel.py').exists()
 assert (config/'KlipperScreen.conf').read_text()==original
 assert json.loads(data.read_text())['profiles']['new']=='keep me'
 assert not (config/'indx-installed-version.json').exists()
print('PASS: package verification, temporary install/update, idempotent menus, exact panel/config rollback, newer calibration data retained.')
