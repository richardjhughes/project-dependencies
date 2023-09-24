import os
import shutil
import platform
import argparse
import zipfile
import subprocess

chmodPath = shutil.which("chmod")

version = "1.11.1"

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


def runCmd(cmd, cwd=None):
    print(f"Running command: {cmd}")
    subprocess.run(cmd, cwd=cwd)


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

    installDir = os.path.join(path, "ninja", platformName)

    return installDir


def isAlreadyInstalled(path):
    installDir = getFullInstallDir(path)

    filesExist = False

    if platform.system() == "Windows":
        filesExist = (os.path.exists(os.path.join(installDir, "ninja.exe")))
    else:
        filesExist = (os.path.exists(os.path.join(installDir, "ninja")))

    return filesExist


def getBinaryOutPath():
    platformName = platform.system()

    binaryOut = os.path.join(os.getcwd(), "lib", platformName)

    return binaryOut


def getOutputZipPath(binaryOutPath):
    platformName = platform.system()

    zipPath = os.path.join(binaryOutPath, f"{version}_{platformName}.zip")

    return zipPath


def install(path):
    binaryPath = getBinaryOutPath()
    zipPath = getOutputZipPath(binaryPath)

    installDir = getFullInstallDir(path)

    createDirectories(installDir)

    with zipfile.ZipFile(zipPath, "r") as zip:
        zip.extractall(installDir)

    # random executable files from the internet may not have
    # permissions to execute
    if platform.system() == "Darwin" or platform.system() == "Linux":
        exePath = os.path.join(installDir, "ninja")
        cmd = [chmodPath, "+x", exePath]
        runCmd(cmd)


print("Installing Ninja...")

args = configureArguments()

if args.version is not None and len(args.version) > 0:
    version = args.version

if isAlreadyInstalled(args.path):
    print("Ninja already installed.")
else:
    install(args.path)

print("Installed Ninja.")