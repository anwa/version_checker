import requests
from packaging import version
import configparser
import logging
import os
import re


logging.basicConfig(
    format="[%(asctime)s] %(levelname)s : %(message)s (Line: %(lineno)d [%(filename)s])",
    datefmt="%d.%m.%Y %H:%M:%S",
    # filename="version_checker.log",
    level=logging.INFO,
    encoding="utf-8",
    handlers=[logging.FileHandler("version_checker.log"), logging.StreamHandler()],
)


# Read the configuration file
config = configparser.ConfigParser()
config.read('version_checker.conf')
base_folder = config.get('main', 'base_folder')

# Ensure that base_folder exists
os.makedirs(base_folder, exist_ok=True)


# Extract the version from the filename
def extract_version_from_filename(filename):
    match = re.search(r'Microsoft\.WindowsTerminal_(\d+\.\d+\.\d+\.\d+)_', filename)
    return match.group(1) if match else None

# Check the current directory for a Microsoft Terminal file
local_version = version.parse('0')
file_to_delete = None
for file in os.listdir(base_folder):
    if file.startswith('Microsoft.WindowsTerminal_') and file.endswith('.msixbundle'):
        extracted_version = version.parse(extract_version_from_filename(file))
        if extracted_version and (extracted_version > local_version):
            if file_to_delete:
                os.remove(os.path.join(base_folder, file_to_delete))
            local_version = extracted_version
            logging.info(f"Found local version:  {local_version.base_version}")
            file_to_delete = file

if local_version.base_version == '0':
    logging.info("No local version found!")
                 
# URL of the GitHub API for the latest release of Microsoft Terminal
api_url = "https://api.github.com/repos/microsoft/terminal/releases/latest"

# Send an API request to GitHub
response = requests.get(api_url)
latest_release_data = response.json()

# Browse the assets and look for the MSIX bundle
msix_bundle_url = None
for asset in latest_release_data.get("assets", []):
    if asset["name"].endswith(".msixbundle"):
        msix_bundle_url = asset["browser_download_url"]
        msix_bundle_name = asset["name"]
        break

# Extract the latest version
latest_release_version = version.parse(latest_release_data.get("tag_name", "").replace('v', ''))
logging.info(f"Found remote version: {latest_release_version.base_version}")

# Compare the latest version with the local version
if latest_release_version > local_version:
    # Download the latest release
    logging.info(f"Download version: {latest_release_version.base_version} to {base_folder}")
    response = requests.get(msix_bundle_url)
    with open(os.path.join(base_folder, msix_bundle_name), "wb") as file:
        file.write(response.content)

    # Delete the older version if it exists
    if file_to_delete:
        logging.info(f"Remove local version:  {local_version.base_version}")
        os.remove(os.path.join(base_folder, file_to_delete))
else:
    logging.info(f"Nothing to do, we have the latest version.")

