# Copyright 2023 Daniel Ragusa

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.







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

    
}

else {
    & $env:SCRIPT_DIR/../venv/Scripts/Activate.ps1
    
}




# Run the Python script
python.exe "$env:SCRIPT_DIR\..\scrapeBot.py"
