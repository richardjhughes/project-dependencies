import os
import shutil
import platform
import argparse
import zipfile

version = "v0.9.0-pre16"

def configureArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", action="store", required=True, help="path to install in")
    parser.add_argument("-v", "--version", action="store", required=False, help="version to install")
    args = parser.parse_args()

    return args


def createDirectories(path):
    print(f"Creating directory: {path}")

    try:
        os.makedirs(path, exist_ok=True)
    except OSError as error:
        print(error)


def getFullInstallDir(path):
    osName = platform.system()

    platformName = ""

    if osName == "Windows":
        platformName = "windows"
    elif osName == "Darwin":
        platformName = "darwin"
    elif osName == "Linux":
        platformName = "linux"
    else:
        platformName = "unknown"

    installDir = os.path.join(path, "sail", platformName)

    return installDir


def isAlreadyInstalled(path):
    installDir = getFullInstallDir(path)

    filesExist = False

    if platform.system() == "Windows":
        filesExist = (os.path.exists(os.path.join(installDir, "SDL2.dll")) and
                      os.path.exists(os.path.join(installDir, "SDL2.lib")) and
                      os.path.exists(os.path.join(installDir, "SDL2main.lib")) and
                      os.path.exists(os.path.join(installDir, "SDL2.exp")) and
                      os.path.exists(os.path.join(installDir, "SDL2-static.lib")) and
                      os.path.exists(os.path.join(installDir, "include")))
    else:
        filesExist = (os.path.exists(os.path.join(installDir, "lib", "libsail.a")) and
                      os.path.exists(os.path.join(installDir, "include")))

    return filesExist


def getBinaryOutPath():
    binaryOut = os.path.join(os.getcwd(), "lib", platform.system())

    return binaryOut


def getOutputZipPath(binaryOutPath):
    zipPath = os.path.join(binaryOutPath, f"{version}_{platform.system()}.zip")

    return zipPath


def install(path):
    binaryPath = getBinaryOutPath()
    zipPath = getOutputZipPath(binaryPath)

    installDir = getFullInstallDir(path)

    createDirectories(installDir)

    with zipfile.ZipFile(zipPath, "r") as zip:
        zip.extractall(installDir)


print("Installing SAIL...")

args = configureArguments()

if args.version is not None and len(args.version) > 0:
    version = args.version

if isAlreadyInstalled(args.path):
    print("SAIL is already installed.")
else:
    install(args.path)

print("Installed SAIL.")
