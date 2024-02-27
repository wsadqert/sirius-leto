Clear-Host

$current_directory = Get-Location

# compiling
pyinstaller --onefile "main.py" --add-data assets:assets --paths src/ --paths venv/Lib/site-packages
pyinstaller --onefile "main_gui.py" --add-data assets:assets --paths src/ --paths venv/Lib/site-packages

# cleaning previous version of `assets`
Set-Location dist/

Remove-Item assets -Recurse -Force -ErrorAction Ignore
Copy-Item ../assets . -Recurse
Remove-Item dist.zip -Recurse -Force -ErrorAction Ignor
Remove-Item datastore -Recurse -Force -ErrorAction Ignore

Write-Output "assets`r`n main.exe`r`n main_gui.exe" | Out-File listfile.txt

# compressing
cmd /c "7z a -mx1 -mmt=12 -tzip dist.zip @listfile.txt"

Set-Location $current_directory
