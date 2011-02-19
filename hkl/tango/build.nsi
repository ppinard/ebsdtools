; Installation NSIS script based on example2.nsi
;
; This script is based on example1.nsi, but it remember the directory, 
; has uninstall support and (optionally) installs start menu shortcuts.
;
; It will install example2.nsi into a directory that the user selects,

;--------------------------------

; The name of the installer
Name "%(name)s"

; The file to write
OutFile "%(name)s_installer.exe"

; The default installation directory
InstallDir $PROGRAMFILES\%(name)s

; Registry key to check for directory (so if you install again, it will 
; overwrite the old one automatically)
InstallDirRegKey HKLM "Software\%(name)s" "Install_Dir"

; Request application privileges for Windows Vista
RequestExecutionLevel admin

;--------------------------------

; Pages

Page components
Page directory
Page instfiles

UninstPage uninstConfirm
UninstPage instfiles

;--------------------------------

; The stuff to install
Section "%(name)s (required)"

  SectionIn RO
  
  ; Set output path to the installation directory.
  SetOutPath $INSTDIR
  
  ; Put file there
  File /r %(dest_dir)s\exe\%(name)s\*.*
  
  ; Write the installation path into the registry
  WriteRegStr HKLM SOFTWARE\%(name)s "Install_Dir" "$INSTDIR"
  
  ; Write key for the Edit with pyFlamenco key
  WriteRegStr HKCR "CHANNEL project file\Shell\Edit" "" ""
  WriteRegStr HKCR "CHANNEL project file\Shell\Edit\command" "" '"$INSTDIR\%(name)s.exe" "%%1"'
  
  ; Write the uninstall keys for Windows
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\%(name)s" "DisplayName" "%(name)s"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\%(name)s" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\%(name)s" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\%(name)s" "NoRepair" 1
  WriteUninstaller "uninstall.exe"
  
SectionEnd

; Optional section (can be disabled by the user)
Section "Start Menu Shortcuts"

  CreateDirectory "$SMPROGRAMS\%(name)s"
  CreateShortCut "$SMPROGRAMS\%(name)s\%(name)s.lnk" "$INSTDIR\%(name)s.exe" "" "$INSTDIR\%(name)s.exe" 0
  
SectionEnd

;--------------------------------

; Uninstaller

Section "Uninstall"
  
  ; Remove registry keys
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\%(name)s"
  DeleteRegKey HKLM SOFTWARE\%(name)s
  DeleteRegKey HKCR "CHANNEL project file\Shell\Edit"

  ; Remove files and uninstaller
  Delete $INSTDIR\*.*
  RMDir  /r $INSTDIR
;  Delete $INSTDIR\uninstall.exe

  ; Remove shortcuts, if any
  Delete "$SMPROGRAMS\%(name)s\*.*"

  ; Remove directories used
  RMDir "$SMPROGRAMS\%(name)s"
  RMDir "$INSTDIR"

SectionEnd
