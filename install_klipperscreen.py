"""Local panel installer with backup. Run on the KlipperScreen computer."""
import argparse,py_compile,shutil,tempfile,time,zipfile,subprocess,os
from pathlib import Path

parser=argparse.ArgumentParser()
parser.add_argument('--klipperscreen-dir',type=Path,required=True)
parser.add_argument('--config-dir',type=Path,required=True)
parser.add_argument('--restart',action='store_true',help='Restart KlipperScreen after copying panels; never runs printer G-code')
args=parser.parse_args()
ks=args.klipperscreen_dir.expanduser().resolve();config=args.config_dir.expanduser().resolve()
if not (ks/'panels').is_dir() or not (ks/'ks_includes').is_dir():raise SystemExit('Not a KlipperScreen source directory')
conf=config/'KlipperScreen.conf'
if not conf.is_file():raise SystemExit('Existing KlipperScreen.conf is required; no configuration is invented')
backup=config/('indx-screen-backup-'+str(time.time_ns()));backup.mkdir()
shutil.copy2(conf,backup/conf.name)
names=['indx_profiles.py','indx_filaments.py','indx_pa.py','indx_flow_tests.py','indx_flow.py','indx_max_flow.py']
with tempfile.TemporaryDirectory() as td,zipfile.ZipFile(Path(__file__).with_name('touchscreen.zip')) as archive:
 stage=Path(td)
 for name in names:
  source=archive.read('touchscreen/'+name).decode('utf-8')
  source=source.replace('/home/sovol/printer_data/config',str(config)).replace('/home/sovol/printer_data/gcodes',str(config.parent/'gcodes'))
  (stage/name).write_text(source,encoding='utf-8');py_compile.compile(str(stage/name),doraise=True)
  existing=ks/'panels'/name
  if existing.exists():shutil.copy2(existing,backup/name)
 for name in ['indx-pa-bases.json','indx-filament-library.json','indx-filament-assignments.json','indx-pa-results.json','indx-tool-setup.json']:
  if (config/name).exists():shutil.copy2(config/name,backup/name)
 for name in names:shutil.copy2(stage/name,ks/'panels'/name)
 if not (config/'indx-pa-bases.json').exists():(config/'indx-pa-bases.json').write_bytes(archive.read('touchscreen/legacy-bases.json'))
 text=conf.read_text(encoding='utf-8')
 for key,label,panel in [('filaments','I miei filamenti','indx_filaments'),('pa','Calibra PA','indx_pa'),('flow','Calibra flow','indx_flow'),('max_flow','Calibra flusso massimo','indx_max_flow')]:
  section='[menu __main indx '+key+']'
  if section not in text:text+='\n'+section+'\nname: '+label+'\nicon: filament\npanel: '+panel+'\n'
 if '[menu __main indx]' not in text:text+='\n[menu __main indx]\nname: INDX\nicon: filament\n'
 temp=conf.with_suffix('.indx-tmp');temp.write_text(text,encoding='utf-8');os.replace(temp,conf)
print('Installed source panels. Backup:',backup)
print('Syntax verified; GTK constructors, menus and physical commissioning still require verification.')
print('No macro, MCU firmware, motion gate or calibration result was changed.')
if args.restart:subprocess.run(['sudo','-n','systemctl','restart','KlipperScreen'],check=True)
