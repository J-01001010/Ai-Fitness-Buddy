[Setup]
AppName=Ai Fitness Buddy
AppVersion=1.0
DefaultDirName={commonpf}\Ai Fitness Buddy
OutputDir=Output
OutputBaseFilename=AiFitnessBuddy
Compression=lzma2
SolidCompression=yes

[Files]
Source: "G:\johnnyworks\ai's\xyz\dist\Ai_Fitness_Buddy.exe"; DestDir: "{app}"
Source: "G:\johnnyworks\ai's\xyz\backend.py"; DestDir: "{app}"
Source: "G:\johnnyworks\ai's\xyz\gym.jpg"; DestDir: "{app}"

[Icons]
Name: "{group}\Ai Fitness Buddy"; Filename: "{app}\Ai_Fitness_Buddy.exe"
Name: "{commondesktop}\Ai Fitness Buddy"; Filename: "{app}\Ai_Fitness_Buddy.exe"; IconFilename: "{app}\icon004.png"
Name: "{commonstartmenu}\Programs\Ai Fitness Buddy"; Filename: "{app}\Ai_Fitness_Buddy.exe"

[Run]
Filename: "{app}\Ai_Fitness_Buddy.exe"; Description: "Launch Your Application"; Flags: nowait postinstall
