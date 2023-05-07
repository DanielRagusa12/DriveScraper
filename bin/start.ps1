# Get the script directory
$env:SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path

# Check if Python and pip are installed
if (-not(Get-Command python.exe -ErrorAction SilentlyContinue) -or -not(Get-Command pip.exe -ErrorAction SilentlyContinue)) {
    Write-Host "Python and/or pip not found. Please download and install them." -ForegroundColor Yellow
    Write-Host "Python download page: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "pip download page: https://pip.pypa.io/en/stable/installation/" -ForegroundColor Yellow
    Exit
}

# Check if venv folder exists
if (-not(Test-Path "$env:SCRIPT_DIR\..\venv")) {
    Write-Host "venv folder not found. Creating venv..." -ForegroundColor Yellow
    python.exe -m venv "$env:SCRIPT_DIR/../venv"

    # Activate the virtual environment
    & $env:SCRIPT_DIR/../venv/Scripts/Activate.ps1

    # Install dependencies
    if (-not(Test-Path "$env:SCRIPT_DIR\..\requirements.txt")) {
        Write-Host "requirements.txt not found. Skipping installation of dependencies." -ForegroundColor Yellow
    } else {
        Write-Host "Installing dependencies..." -ForegroundColor Yellow
        pip.exe install -r "$env:SCRIPT_DIR\..\requirements.txt"
    }

    # Copy themes.py from local directory to venv/Lib/site-packages/inquirer/ directory
    $local_themes_path = "$env:SCRIPT_DIR\..\lib\themes.py"
    Write-Host "Local themes.py path: $local_themes_path"
    $venv_themes_path = "$env:SCRIPT_DIR\..\venv\Lib\site-packages\inquirer\themes.py"
    if (Test-Path $local_themes_path) {
        Copy-Item $local_themes_path $venv_themes_path -Force
        Write-Host "themes.py copied to venv\Lib\site-packages\inquirer\" -ForegroundColor Green
    } else {
        Write-Host "themes.py not found in local directory. Skipping copy." -ForegroundColor Yellow
    }
}

else {
    & $env:SCRIPT_DIR/../venv/Scripts/Activate.ps1
    
}




# Run the Python script
python.exe "$env:SCRIPT_DIR\..\scrapeBot.py"
