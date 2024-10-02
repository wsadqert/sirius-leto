Clear-Host

$current_directory = Get-Location

while (true) {
    if (!(Test-Path "venv/")) {
        Write-Host "Virtual environment is not detected. Provide path to it or type 'new' to create venv or press ENTER/RETURN to use global interpreter: "
        $command = Read-Host

        if ($command -eq "new") {
            Write-Host "Creating..." -NoNewline -ForegroundColor Cyan
            python -m venv venv/
            Write-Host "`rCreated!   "
            $venv = "venv"
            break
        } else {
            $venv = $command
            if (Test-Path $venv) { break }
        }
    } else {
        $venv = "venv"
        break
    }
}

Write-Host $venv

# compiling
if ($venv -ne "") {
    $site_packages = "C:\\Users\\Matvey\\PycharmProjects\\sirius_leto_repository\\venv\\Lib\\site-packages"
    # pyinstaller --onefile "main.py" --add-data assets:assets --paths src/ --paths $site_packages
    pyinstaller --onefile "main_gui.py" --add-data assets:assets --paths src/ --paths $site_packages
} else {  # using global interpreter
    # pyinstaller --onefile "main.py" --add-data assets:assets --paths src/
    pyinstaller --onefile "main_gui.py" --add-data assets:assets --paths src/
}

# cleaning previous version of `assets`
Set-Location dist/

Remove-Item assets -Recurse -Force -ErrorAction Ignore
Copy-Item ../assets . -Recurse
Remove-Item dist.zip -Recurse -Force -ErrorAction Ignor
Remove-Item datastore -Recurse -Force -ErrorAction Ignore

Write-Output "assets`r`n main.exe`r`n main_gui.exe" | Out-File "listfile.txt"

# compressing
cmd /c "7z a -mx1 -mmt=12 -tzip dist.zip @listfile.txt"

# cleaning temporary file
Remove-Item "listfile.txt"

Set-Location $current_directory
