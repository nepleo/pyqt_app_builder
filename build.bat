@echo off

.venv\Scripts\python -m PyInstaller -F -w -i resource\icons\logo.ico --distpath .\build .\main.py

pause
