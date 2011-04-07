; Installation NSIS script based on example2.nsi
;
; This script is based on example1.nsi, but it remember the directory, 
; has uninstall support and (optionally) installs start menu shortcuts.
;
; It will install example2.nsi into a directory that the user selects,

;--------------------------------

; The name of the installer
Name "${NAME}"

; The file to write
OutFile "${DIST.DIR}\${NAME}_installer.exe"

; The default installation directory
InstallDir $PROGRAMFILES\${NAME}

; Registry key to check for directory (so if you install again, it will 
; overwrite the old one automatically)
InstallDirRegKey HKLM "Software\${NAME}" "Install_Dir"

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
Section "${NAME} (required)"

  SectionIn RO
  
  ; Set output path to the installation directory.
  SetOutPath $INSTDIR
  
  ; Put file there
  File /r ${SRC.DIR}\*.*
  
  ; Write the installation path into the registry
  WriteRegStr HKLM SOFTWARE\${NAME} "Install_Dir" "$INSTDIR"
  
  ; Write key for the View with pyTango key
  WriteRegStr HKCR "CHANNEL project file\Shell\View" "" ""
  WriteRegStr HKCR "CHANNEL project file\Shell\View\command" "" '"$INSTDIR\${NAME}.exe" "%%1"'
  
  ; Write the uninstall keys for Windows
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${NAME}" "DisplayName" "${NAME}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${NAME}" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${NAME}" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${NAME}" "NoRepair" 1
  WriteUninstaller "uninstall.exe"
  
SectionEnd

; Optional section (can be disabled by the user)
Section "Start Menu Shortcuts"

  CreateDirectory "$SMPROGRAMS\${NAME}"
  CreateShortCut "$SMPROGRAMS\${NAME}\${NAME}.lnk" "$INSTDIR\${NAME}.exe" "" "$INSTDIR\${NAME}.exe" 0
  
SectionEnd

;--------------------------------

; Uninstaller

Section "Uninstall"
  
  ; Remove registry keys
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${NAME}"
  DeleteRegKey HKLM SOFTWARE\${NAME}
  DeleteRegKey HKCR "CHANNEL project file\Shell\View"

  ; Remove files and uninstaller
  Delete $INSTDIR\*.*
  RMDir  /r $INSTDIR
;  Delete $INSTDIR\uninstall.exe

  ; Remove shortcuts, if any
  Delete "$SMPROGRAMS\${NAME}\*.*"

  ; Remove directories used
  RMDir "$SMPROGRAMS\${NAME}"
  RMDir "$INSTDIR"

SectionEnd
