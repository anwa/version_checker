import requests
from packaging import version
import os
import re


# Funktion, um die Version aus dem Dateinamen zu extrahieren
def extract_version_from_filename(filename):
    match = re.search(r'VSCodeUserSetup-x64-(\d+\.\d+\.\d+)\.exe', filename)
    return match.group(1) if match else None

# Überprüfen Sie das aktuelle Verzeichnis nach einer VSCode Installationsdatei
local_version = '0'
file_to_delete = None
for file in os.listdir('.'):
    if file.startswith('VSCodeUserSetup-x64-') and file.endswith('.exe'):
        extracted_version = extract_version_from_filename(file)
        if extracted_version and (extracted_version > local_version):
            if file_to_delete:
                os.remove(file_to_delete)
            local_version = extracted_version
            file_to_delete = file

# URL der GitHub API für das neueste Release von Visual Studio Code
api_url = "https://api.github.com/repos/microsoft/vscode/releases/latest"

# API-Anfrage an GitHub senden
response = requests.get(api_url)
latest_release_data = response.json()

# Neueste Version extrahieren
latest_release_version = latest_release_data.get("tag_name", "").replace('v', '')

# Vergleichen Sie die neueste Version mit der lokalen Version
if latest_release_version > local_version:
    # Neuestes Release herunterladen
    download_url = "https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user"
    response = requests.get(download_url)
    download_filename = f'VSCodeUserSetup-x64-{latest_release_version}.exe'
    with open(download_filename, "wb") as file:
        file.write(response.content)

    # Löschen der älteren Version, falls vorhanden
    if file_to_delete:
        os.remove(file_to_delete)