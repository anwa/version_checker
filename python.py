import configparser
import logging
import os
import re
import sys
from urllib.parse import unquote, urlparse

import requests
from bs4 import BeautifulSoup
from packaging import version


# Setup logging
def set_logging():
    logging.basicConfig(
        format="[%(asctime)s] %(levelname)s : %(message)s (Line: %(lineno)d [%(filename)s])",
        datefmt="%d.%m.%Y %H:%M:%S",
        # filename="version_checker.log",
        level=logging.INFO,
        encoding="utf-8",
        handlers=[logging.FileHandler("version_checker.log"), logging.StreamHandler()],
    )


# Read the configuration file
def read_config():
    config = configparser.ConfigParser()
    config.read("version_checker.conf")
    return config


# Extract the version from the filename
def extract_version_from_filename(filename):
    match = re.search(r"python-(\d+\.\d+\.\d+)-amd64\.exe", filename)
    return version.parse(match.group(1) if match else None)


def extract_version_from_url(url):
    parsed_url = urlparse(url)
    filename = unquote(parsed_url.path.split("/")[-1])
    match = re.search(r"python-(\d+\.\d+\.\d+)-amd64\.exe", filename)
    return version.parse(match.group(1) if match else None)


def extract_filename_from_url(url):
    parsed_url = urlparse(url)
    return unquote(parsed_url.path.split("/")[-1])


def download_file(url, directory):
    response = requests.get(url)
    filename = extract_filename_from_url(url)
    if response.status_code == 200:
        with open(os.path.join(directory, filename), "wb") as file:
            file.write(response.content)
        logging.info(f"Finished download: {filename}")
    else:
        logging.error(f"Error: {response.status_code}, downloading file: {filename}")


def find_local_file(app_folder):
    for local_file in os.listdir(app_folder):
        if local_file.startswith("python-") and local_file.endswith(".exe"):
            return local_file
    return None


# Funktion, um die installierte Git-Version zu ermitteln (windows)
def get_installed_version():
    try:
        python_version = sys.version
        version_installed = python_version.split()[0]
        # Konvertieren des Strings in ein Version-Objekt
        return version.parse(version_installed)
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")


# Get url for download
def get_latest_stable_version():
    url = "https://www.python.org/downloads/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Suchen nach dem direkten Download-Link
    links = soup.find_all("a", {"class": "button"})
    for link in links:
        if "href" in link.attrs:
            href = link.attrs["href"]
            if href.endswith("amd64.exe"):
                return href


def python(app_folder):
    # Check app_folder directory for a Python Installer
    file_to_delete = None
    local_file = find_local_file(app_folder)
    if local_file:
        local_version = extract_version_from_filename(local_file)
        if local_version:
            logging.info(f"Found local version:  {local_version.base_version}")
            file_to_delete = local_file
        else:
            logging.error(f"Found local file: {local_file} Can'n get version!")
            sys.exit(1)
    else:
        local_version = version.parse("0")
        logging.info("No local version found!")

    url = get_latest_stable_version()
    latest_version = extract_version_from_url(url)

    logging.info(f"Found remote version: {latest_version.base_version}")

    # Compare the latest version with the local version
    if latest_version > local_version:
        # Download the latest release
        logging.info(f"Download version: {latest_version.base_version} to {app_folder}")
        download_file(url, app_folder)

        # Delete the older version if it exists
        if file_to_delete:
            logging.info(f"Remove local version:  {local_version.base_version}")
            os.remove(os.path.join(app_folder, file_to_delete))
    else:
        logging.info(f"Nothing to do, we have the latest version.")

    installed_version = get_installed_version()
    if latest_version > installed_version:
        logging.warningo(f"Local version {installed_version.base_version} is outdated!")
    else:
        logging.info(f"Found installed version:  {installed_version.base_version}")


def main():
    set_logging()
    config = read_config()
    base_folder = config.get("main", "base_folder")

    # Ensure that base_folder exists
    os.makedirs(base_folder, exist_ok=True)
    python(base_folder)
    return 0


if __name__ == "__main__":
    sys.exit(main())
