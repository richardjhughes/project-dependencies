import os
import shutil
import platform
import argparse
import zipfile

version = "3.35.5"

def configureArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", action="store", required=True, help="path to install in")
    args = parser.parse_args()

    return args


def createDirectories(path):
    print(f"Creating directory: {path}")

    try:
        os.makedirs(path, exist_ok=True)
    except OSError as error:
        print(error)


def getFullInstallDir(path):
    installDir = os.path.join(path, "sqlite3")

    return installDir


def isAlreadyInstalled(path):
    installDir = getFullInstallDir(path)

    filesExist = (os.path.exists(os.path.join(installDir, "CMakeLists.txt")) and
                  os.path.exists(os.path.join(installDir, "src", "sqlite3.c")) and
                  os.path.exists(os.path.join(installDir, "sqlite3.h")) and
                  os.path.exists(os.path.join(installDir, "sqlite3ext.h")))

    return filesExist

def getBinaryOutPath():
    binaryOut = os.path.join(os.getcwd(), "lib")

    return binaryOut


def getOutputZipPath(binaryOutPath):
    zipPath = os.path.join(binaryOutPath, f"{version}.zip")

    return zipPath


def install(path):
    binaryPath = getBinaryOutPath()
    zipPath = getOutputZipPath(binaryPath)

    installDir = getFullInstallDir(path)

    createDirectories(installDir)

    with zipfile.ZipFile(zipPath, "r") as zip:
        zip.extractall(installDir)


print("Installing sqlite3...")

args = configureArguments()

if isAlreadyInstalled(args.path):
    print("sqlite3 already installed.")
else:
    install(args.path)

print("Installed sqlite3.")
