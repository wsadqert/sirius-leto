Clear-Host
pyinstaller --onefile main.py --add-data assets:assets --paths src/
Remove-Item dist/assets -Recurse -Force -ErrorAction Ignore
Copy-Item assets dist/
Remove-Item dist/dist.zip -Recurse -Force -ErrorAction Ignore
Remove-Item dist/datastore -Recurse -Force -ErrorAction Ignore
7z a -tzip dist/dist.zip dist/
