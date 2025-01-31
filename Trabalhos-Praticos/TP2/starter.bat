@echo off

set fileBaseName=test

set goFile=C:\Users\danie\Desktop\Uni\3ano\PLC\TP2_Ze_final\%fileBaseName%.go

C:\Python312\python.exe C:\Users\danie\Desktop\Uni\3ano\PLC\TP2_Ze_final\compiler.py %goFile%

set vmFile=C:\Users\danie\Desktop\Uni\3ano\PLC\TP2_Ze_final\%fileBaseName%.vm

powershell -Command "Get-Content '%vmFile%' | clip"

echo Done!