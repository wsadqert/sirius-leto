cls
pyinstaller --onefile main.py --add-data assets:assets --paths src/
rmdir /s dist/assets
copy assets dist/
rm dist/dist.zip
rmdir /s dist/datastore
7z a -tzip dist/dist.zip dist/
