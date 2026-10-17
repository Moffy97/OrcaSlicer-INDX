#ifndef AppSource
  #define AppSource "app"
#endif
#ifndef PackageSource
  #define PackageSource "package"
#endif
#ifndef OutputRoot
  #define OutputRoot "dist"
#endif
[Setup]
AppId=OrcaSlicerINDXSV08MaxPreview
AppName=OrcaSlicer INDX SV08 Max
AppVersion=0.3.0-preview
AppVerName=OrcaSlicer INDX SV08 Max 0.3.0 preview
AppPublisher=OrcaSlicer INDX community project
AppPublisherURL=https://github.com/Moffy97/OrcaSlicer-INDX
AppSupportURL=https://github.com/Moffy97/OrcaSlicer-INDX/issues
DefaultDirName={localappdata}\Programs\OrcaSlicer-INDX-SV08Max
DefaultGroupName=OrcaSlicer INDX SV08 Max
DisableProgramGroupPage=yes
DisableDirPage=no
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0
OutputDir={#OutputRoot}
OutputBaseFilename=OrcaSlicer-INDX-SV08Max-0.3.0-preview-Setup-x64
Compression=lzma2/fast
SolidCompression=yes
LZMANumBlockThreads=2
WizardStyle=modern
SetupIconFile={#AppSource}\resources\images\OrcaSlicer.ico
UninstallDisplayIcon={app}\app\orca-slicer.exe
CloseApplications=no
RestartApplications=no
AllowNoIcons=yes
SetupLogging=yes
[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "italian"; MessagesFile: "compiler:Languages\Italian.isl"
[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
[Files]
Source: "{#AppSource}\*"; DestDir: "{app}\app"; Excludes: "*.pdb,*.log,__pycache__\*,.git\*,logs\*"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#PackageSource}\dati\*"; DestDir: "{app}\dati"; Flags: onlyifdoesntexist uninsneveruninstall recursesubdirs createallsubdirs; Check: SeedInitialData
Source: "{#PackageSource}\Avvia-Orca-INDX.cmd"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#PackageSource}\Guida_completa_INDX_Orca_KlipperScreen.pdf"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#PackageSource}\LEGGIMI.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#PackageSource}\LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#PackageSource}\OrcaSlicer-INDX.patch"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#PackageSource}\PLUGIN_KLIPPERSCREEN_SV08MAX.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#PackageSource}\prepare_source.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#PackageSource}\profili\*"; DestDir: "{app}\profili"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#PackageSource}\UGELLI_MANUALI_AUTOMATICI.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#PackageSource}\UPSTREAM.json"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#PackageSource}\windows-installer.iss"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#PackageSource}\WINDOWS_INSTALLER.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#PackageSource}\windows-installer.iss"; DestDir: "{app}"; Flags: ignoreversion
[Icons]
Name: "{group}\OrcaSlicer INDX SV08 Max"; Filename: "{app}\app\orca-slicer.exe"; Parameters: "--datadir ""{app}\dati"""; WorkingDir: "{app}"
Name: "{group}\Uninstall OrcaSlicer INDX SV08 Max"; Filename: "{uninstallexe}"
Name: "{autodesktop}\OrcaSlicer INDX SV08 Max"; Filename: "{app}\app\orca-slicer.exe"; Parameters: "--datadir ""{app}\dati"""; WorkingDir: "{app}"; Tasks: desktopicon
[Code]
var
  ShouldSeedData: Boolean;
function SeedInitialData: Boolean;
begin
  Result := ShouldSeedData;
end;
function PrepareToInstall(var NeedsRestart: Boolean): String;
begin
  ShouldSeedData := not FileExists(ExpandConstant('{app}\dati\OrcaSlicer.conf'));
  Result := '';
end;
