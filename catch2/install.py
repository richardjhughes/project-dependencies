import os
import shutil
import platform
import argparse
import subprocess
import zipfile

version = "2.13.6"
gitURL = "https://github.com/catchorg/Catch2.git"

gitPath = shutil.which("git")

def configureArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", action="store", required=True, help="path to install in")
    args = parser.parse_args()

    return args


def createDirectories(path):
    print(f"Creating directory: {path}")

    try:
        os.makedirs(path)
    except OSError as error:
        print(error)


def removeDirectory(path):
    print(f"Removing directory: {path}")

    try:
        shutil.rmtree(path)
    except OSError as error:
        print(error)


def runCmd(cmd, cwd=None):
    print(f"Running command: {cmd}")
    subprocess.run(cmd, cwd=cwd)


def getFullInstallDir(path):
    installDir = os.path.join(path, "catch2")

    return installDir


def isAlreadyInstalled(path):
    installDir = getFullInstallDir(path)

    filesExist = os.path.exists(installDir)

    return filesExist


def install(path):
    cwd = os.getcwd()

    # get the source code
    tempDirPath = os.path.join(cwd, "__temp", "catch2")
    createDirectories(tempDirPath)

    os.chdir(tempDirPath)

    cmd = [gitPath, "clone", f"{gitURL}"]
    runCmd(cmd)

    os.chdir(os.path.join(os.getcwd(), "catch2"))

    # checkout the version we want
    cmd = [gitPath, "checkout", f"tags/v{version}", "-b", f"v{version}"]
    runCmd(cmd)

    installDir = getFullInstallDir(path)

    # copy the code
    # git archive will only create a package file from the repo, so
    # package as a zip then unzip to the install directory
    archivePath = os.path.join(cwd, "__temp", "catch2.zip")
    cmd = [gitPath, "archive", "--output", f"{archivePath}", "HEAD"]
    runCmd(cmd)

    createDirectories(installDir)

    with zipfile.ZipFile(archivePath, "r") as zip:
        zip.extractall(installDir)

    os.chdir(cwd)


print("Installing catch2...")

args = configureArguments()

if isAlreadyInstalled(args.path):
    print("catch2 already installed.")
else:
    install(args.path)

print("Installed catch2.")