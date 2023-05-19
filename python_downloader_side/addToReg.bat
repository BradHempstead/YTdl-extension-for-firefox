@echo off

REG ADD HKEY_CURRENT_USER\Software\Mozilla\NativeMessagingHosts\ytdlfirefox /d %cd%\ytdlfirefox.json
REG ADD HKEY_LOCAL_MACHINE\Software\Mozilla\NativeMessagingHosts\ytdlfirefox /d %cd%\ytdlfirefox.json
