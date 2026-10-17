"""Install the SV08 Max INDX KlipperScreen add-on; no firmware or motion."""
import argparse
from pathlib import Path
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--install', action='store_true', help='Install panels and automatic sync service, then restart KlipperScreen')
    parser.add_argument('--check', action='store_true', help='Check package without changing the printer')
    parser.add_argument('--klipperscreen-dir', type=Path, default=Path.home()/'KlipperScreen')
    parser.add_argument('--config-dir', type=Path, default=Path.home()/'printer_data/config')
    parser.add_argument('--rollback', type=Path, help='Restore a backup made by the installer')
    args = parser.parse_args()
    if args.install and (args.check or args.rollback):
        parser.error('--install cannot be combined with --check or --rollback')
    root = Path(__file__).resolve().parent
    installer = root/'install_klipperscreen.py'
    subprocess.run([sys.executable, str(installer), '--check'], check=True)
    if args.check or not (args.install or args.rollback):
        print('Package checked. Use --install on the SV08 Max host to enable the add-on.')
        return
    if sys.platform != 'linux':
        parser.error('Install/rollback must run on the Linux host running KlipperScreen')
    command = [sys.executable, str(installer), '--klipperscreen-dir', str(args.klipperscreen_dir.expanduser()),
               '--config-dir', str(args.config_dir.expanduser()), '--restart']
    if args.rollback:
        command += ['--rollback', str(args.rollback.expanduser())]
    else:
        command += ['--sync-service']
    subprocess.run(command, check=True)


if __name__ == '__main__':
    main()
