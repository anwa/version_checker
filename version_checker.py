import configparser
import logging
import os
import sys

from bitwarden import bitwarden
from git import git
from powershell import powershell
from python import python
from sourcetree import sourcetree
from terminal import terminal
from tortoise_git import tortoise_git
from vscode import vscode

# Setup logging
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
config.read("version_checker.conf")
base_folder = config.get("main", "base_folder")


def main():
    # Ensure that base_folder exists
    os.makedirs(base_folder, exist_ok=True)

    logging.info("Checking PowerShell...")
    powershell(base_folder)

    logging.info("Checking Windows Terminal...")
    terminal(base_folder)
    logging.info("Checking Visual Studio Code...")
    vscode(base_folder)
    logging.info("Checking Git...")
    git(base_folder)
    logging.info("Checking TortoiseGit...")
    tortoise_git(base_folder)
    logging.info("Checking SourceTree...")
    sourcetree(base_folder)
    logging.info("Checking Python...")
    python(base_folder)
    logging.info("Checking Bitwarden...")
    bitwarden(base_folder)

    return 0


if __name__ == "__main__":
    sys.exit(main())
