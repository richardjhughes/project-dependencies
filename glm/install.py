import os
import shutil
import platform
import argparse
import subprocess
import zipfile

version = "0.9.9.8"
gitURL = "https://github.com/g-truc/glm.git"

gitPath = shutil.which("git")

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
    installDir = os.path.join(path, "glm")

    return installDir


def isAlreadyInstalled(path):
    installDir = getFullInstallDir(path)

    filesExist = os.path.exists(installDir)

    return filesExist


def install(path):
    cwd = os.getcwd()

    # get the source code
    tempDirPath = os.path.join(cwd, "__temp", "glm")
    createDirectories(tempDirPath)

    os.chdir(tempDirPath)

    cmd = [gitPath, "clone", f"{gitURL}"]
    runCmd(cmd)

    os.chdir(os.path.join(os.getcwd(), "glm"))

    # checkout the version we want
    cmd = [gitPath, "checkout", f"tags/{version}", "-b", f"{version}"]
    runCmd(cmd)

    installDir = getFullInstallDir(path)

    # copy the code
    # git archive will only create a package file from the repo, so
    # package as a zip then unzip to the install directory
    archivePath = os.path.join(cwd, "__temp", "glm.zip")
    cmd = [gitPath, "archive", "--output", f"{archivePath}", "HEAD"]
    runCmd(cmd)

    createDirectories(installDir)

    with zipfile.ZipFile(archivePath, "r") as zip:
        zip.extractall(installDir)

    os.chdir(cwd)


print("Installing glm...")

args = configureArguments()

if args.version is not None and len(args.version) > 0:
    version = args.version

if isAlreadyInstalled(args.path):
    print("glm already installed.")
else:
    install(args.path)

print("Installed glm.")