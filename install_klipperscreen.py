"""Verified local panel update with preview, backup and rollback. No printer G-code."""
import argparse,hashlib,json,os,py_compile,re,shutil,subprocess,tempfile,time,zipfile
from pathlib import Path
NAMES=['indx_profiles.py','indx_filaments.py','indx_pa.py','indx_flow_tests.py','indx_flow.py','indx_max_flow.py','indx_commissioning.py','indx_setup.py','indx_tools.py','indx_machine.py','indx_machine_panel.py','indx_dashboard.py','indx_ui.py']
ASSETS=['indx-ui.css']

def target_file(name,ks,config):
 if name in ('KlipperScreen.conf','indx-installed-version.json'):return config/name
 if name=='indx-ui.css':return ks/'styles/indx-studio/style.css'
 return ks/'panels'/name

def package(root):
 sums={line.split('  ',1)[1]:line.split('  ',1)[0] for line in (root/'SHA256SUMS').read_text().splitlines()}
 for name in ('touchscreen.zip','VERSION.json'):
  if hashlib.sha256((root/name).read_bytes()).hexdigest()!=sums.get(name):raise ValueError('Checksum mismatch: '+name)
 version=json.loads((root/'VERSION.json').read_text())
 if version.get('protocols')!={'catalog':2,'library':3,'hardware':2}:raise ValueError('Unsupported protocol versions')
 return version

def restore(backup,ks,config):
 manifest=json.loads((backup/'rollback.json').read_text())
 if manifest.get('ks')!=str(ks) or manifest.get('config')!=str(config):raise ValueError('Backup belongs to a different installation')
 for name,digest in manifest['files'].items():
  if name not in NAMES+ASSETS+['KlipperScreen.conf','indx-installed-version.json']:raise ValueError('Unexpected backup file')
  if digest is not None and hashlib.sha256((backup/name).read_bytes()).hexdigest()!=digest:raise ValueError('Damaged backup: '+name)
 for name,digest in manifest['files'].items():
  target=target_file(name,ks,config)
  if digest is None:target.unlink(missing_ok=True)
  else:shutil.copy2(backup/name,target)

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--klipperscreen-dir',type=Path);parser.add_argument('--config-dir',type=Path)
 parser.add_argument('--check',action='store_true',help='Verify package, protocols and syntax without installing')
 parser.add_argument('--rollback',type=Path,help='Restore named backup; keeps current filament/calibration data')
 parser.add_argument('--restart',action='store_true',help='Restart KlipperScreen after successful install/rollback')
 args=parser.parse_args();root=Path(__file__).resolve().parent
 if not args.check and (not args.klipperscreen_dir or not args.config_dir):parser.error('Install/rollback require both directories')
 if args.check and (args.rollback or args.restart):parser.error('--check cannot be combined with rollback or restart')
 ks=args.klipperscreen_dir.expanduser().resolve() if args.klipperscreen_dir else None
 config=args.config_dir.expanduser().resolve() if args.config_dir else None
 if ks and (not (ks/'panels').is_dir() or not (ks/'ks_includes').is_dir()):raise ValueError('Not a KlipperScreen source directory')
 if config and not (config/'KlipperScreen.conf').is_file():raise ValueError('Existing KlipperScreen.conf is required')
 if args.rollback:
  restore(args.rollback.expanduser().resolve(),ks,config);print('Panel/config rollback completed. Current filament/calibration data preserved.')
 else:
  version=package(root)
  with tempfile.TemporaryDirectory() as td,zipfile.ZipFile(root/'touchscreen.zip') as archive:
   stage=Path(td)
   for name in NAMES:
    source=archive.read('touchscreen/'+name).decode('utf-8')
    if config:source=source.replace('/home/sovol/printer_data/config',config.as_posix()).replace('/home/sovol/printer_data/gcodes',(config.parent/'gcodes').as_posix())
    (stage/name).write_text(source,encoding='utf-8');py_compile.compile(str(stage/name),doraise=True)
   for name in ASSETS:(stage/name).write_bytes(archive.read('touchscreen/'+name))
   if args.check:print('Package, protocols, theme assets and panel syntax verified:',version['version']);return
   backup=Path(tempfile.mkdtemp(prefix='indx-screen-backup-',dir=config))
   manifest={'ks':str(ks),'config':str(config),'files':{}}
   for name in NAMES+ASSETS+['KlipperScreen.conf','indx-installed-version.json']:
    target=target_file(name,ks,config)
    manifest['files'][name]=hashlib.sha256(target.read_bytes()).hexdigest() if target.exists() else None
    if target.exists():shutil.copy2(target,backup/name)
   (backup/'rollback.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
   text=(config/'KlipperScreen.conf').read_text(encoding='utf-8')
   def theme(match):
    section=match[0]
    return re.sub(r'^theme\s*[:=].*$', 'theme: indx-studio',section,flags=re.M) if re.search(r'^theme\s*[:=]',section,re.M) else section.rstrip()+'\ntheme: indx-studio\n\n'
   text=re.sub(r'^\[main\][^\n]*\n.*?(?=^\[|\Z)',theme,text,flags=re.M|re.S)
   for key,label,panel in [('filaments','I miei filamenti','indx_filaments'),('pa','Calibra PA','indx_pa'),('flow','Calibra flow','indx_flow'),('max_flow','Calibra flusso massimo','indx_max_flow'),('setup','Collaudo INDX','indx_setup'),('tools','Tool configurati','indx_tools'),('machine','Dock e offset','indx_machine_panel')]:
    section='[menu __main indx '+key+']'
    if section not in text:text+='\n'+section+'\nname: '+label+'\nicon: filament\npanel: '+panel+'\n'
   if '[menu __main indx]' not in text:text+='\n[menu __main indx]\nname: INDX\nicon: filament\n'
   def dashboard(match):
    section=re.sub(r'^name:.*$', 'name: INDX',match[0],flags=re.M)
    return re.sub(r'^panel:.*$', 'panel: indx_dashboard',section,flags=re.M) if re.search(r'^panel:',section,re.M) else section.rstrip()+'\npanel: indx_dashboard\n\n'
   text=re.sub(r'^\[menu __main indx\][^\n]*\n.*?(?=^\[|\Z)',dashboard,text,flags=re.M|re.S)
   try:
    for name in NAMES:shutil.copy2(stage/name,ks/'panels'/name)
    theme_dir=ks/'styles/indx-studio';theme_dir.mkdir(parents=True,exist_ok=True)
    shutil.copy2(stage/'indx-ui.css',theme_dir/'style.css')
    images=ks/'styles/material-dark/images'
    if images.is_dir() and not (theme_dir/'images').exists():
     try:os.symlink(images,theme_dir/'images',target_is_directory=True)
     except OSError:shutil.copytree(images,theme_dir/'images')
    temp=config/'KlipperScreen.conf.indx-tmp';temp.write_text(text,encoding='utf-8');os.replace(temp,config/'KlipperScreen.conf')
    (config/'indx-installed-version.json').write_text(json.dumps(version,indent=2),encoding='utf-8')
    if not (config/'indx-pa-bases.json').exists():(config/'indx-pa-bases.json').write_bytes(archive.read('touchscreen/legacy-bases.json'))
   except Exception:
    restore(backup,ks,config);raise
   print('Installed preview',version['version'],'Backup:',backup)
   print('GTK display and physical commissioning require on-machine testing. No firmware or movement gate changed.')
 if args.restart:subprocess.run(['sudo','-n','systemctl','restart','KlipperScreen'],check=True)

if __name__=='__main__':main()
