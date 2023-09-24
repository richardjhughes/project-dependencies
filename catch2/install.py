import os
import shutil
import platform
import argparse
import zipfile

version = "3.4.0"

def configureArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", action="store", required=True, help="path to install in")
    parser.add_argument("-v", "--version", action="store", required=False, help="version to install")
    args = parser.parse_args()

    return args


def createDirectories(path):
    print(f"Creating directory: {path}")

    try:
        os.makedirs(path)
    except OSError as error:
        print(error)


def getFullInstallDir(path):
    installDir = os.path.join(path, "catch2")

    return installDir


def isAlreadyInstalled(path):
    installDir = getFullInstallDir(path)

    filesExist = (os.path.exists(os.path.join(installDir, "include", "catch2", "catch.hpp")) and
                  os.path.exists(os.path.join(installDir, "lib", "cmake", "Catch2", "Catch.cmake")))

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


print("Installing Catch2...")

args = configureArguments()

if args.version is not None and len(args.version) > 0:
    version = args.version

if isAlreadyInstalled(args.path):
    print("Catch2 already installed.")
else:
    install(args.path)

print("Installed Catch2.")
