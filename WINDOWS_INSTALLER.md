# OrcaSlicer INDX SV08 Max - Windows installer

Download `OrcaSlicer-INDX-SV08Max-0.3.1-preview-Setup-x64.exe` from this repository's release Assets. Run it and choose English or Italian. It installs for the current Windows user; the default location is `%LOCALAPPDATA%\Programs\OrcaSlicer-INDX-SV08Max`. A Start menu shortcut is created, and a desktop shortcut is optional. Installation does not launch Orca automatically.

The shortcut launches `app\orca-slicer.exe --datadir "INSTALL_FOLDER\dati"`. This is a separate data directory from official Orca, the other INDX edition and the previously used portable copy. Existing settings are not imported automatically. Export/import presets yourself if needed. Generic starts in English; the interface language can be changed in preferences.

Initial data is copied only when `dati\OrcaSlicer.conf` does not exist. Updates leave the existing data directory untouched. Uninstall removes application files and shortcuts but preserves user data. Choose a writable per-user install location; an administrator-protected folder is not suitable for this data layout.

The installer does not install firmware, change printer files, install KlipperScreen, connect to a printer or register model file associations. The application is a community preview and the installer is not digitally signed. The corresponding portable ZIP contains the same updated application.

## Rebuild

Use Inno Setup 6.7.3 or a compatible release. `windows-installer.iss` accepts `/DAppSource=PATH` for the application tree and `/DPackageSource=PATH` for the profile/document tree (with `dati`), plus `/DOutputRoot=PATH` for the output folder. The application must be the binary corresponding to `OrcaSlicer-INDX.patch` and `UPSTREAM.json`; source and license files are included in the installed package. Keep personal printer addresses and calibration data out of the package.

Example: `ISCC.exe /DAppSource=C:\build\app /DPackageSource=C:\build\package /DOutputRoot=C:\build\out windows-installer.iss`.
