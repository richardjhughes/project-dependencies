import os
import shutil
import platform
import argparse
import subprocess
import zipfile

version = "3.35.5"
gitUrl = "https://github.com/sqlite/sqlite.git"

downloadURL = ""

gitPath = shutil.which("git")
curlPath = shutil.which("curl")
shPath = shutil.which("sh")
makePath = shutil.which("make")

def configureArguments():
    parser = argparse.ArgumentParser()
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


def runCmdIgnoreError(cmd):
    print(f"Running command: {cmd}")
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to run cmd: {cmd}")
        return False
    else:
        print(f"Failed to run cmd with unknown error: {cmd}")
        return False


def build(tempDirPath):
    print("Starting build...")

    if platform.system() == "Windows":
        print("Building on Windows is not supported.")
        return

    createDirectories(tempDirPath)

    os.chdir(tempDirPath)

    # get the latest code
    cmd = [gitPath, "clone", f"{gitUrl}"]
    runCmd(cmd)

    os.chdir(os.path.join(os.getcwd(), "sqlite"))

    # checkout the version we want
    cmd = [gitPath, "checkout", f"tags/{version}", "-b", f"{version}"]
    runCmd(cmd)

    cmd = [shPath, "./configure"]
    runCmd(cmd)

    cmd = [makePath, "sqlite3.c"]
    runCmd(cmd)

    os.chdir(cwd)

    print("Finished build.")


def saveResults(tempDirPath):
    print("Saving results...")

    resultsPath = os.path.join(tempDirPath, "sqlite")

    destLibDir = os.path.join(os.getcwd(), "lib")

    # for CMakeLists.txt
    supportingFilesPath = os.getcwd()

    saveBinaries(supportingFilesPath, destLibDir, resultsPath)

    print("Saved results.")


def saveBinaries(supportingFilesPath, destLibDir, resultsPath):
    createDirectories(destLibDir)

    zipDir = getZipPath(destLibDir)

    with zipfile.ZipFile(zipDir, "w") as zip:
        zip.write(os.path.join(supportingFilesPath, "CMakeLists.txt"), os.path.join("CMakeLists.txt"))
        zip.write(os.path.join(resultsPath, "sqlite3.h"), os.path.join("include", "sqlite3.h"))
        zip.write(os.path.join(resultsPath, "sqlite3ext.h"), os.path.join("include", "sqlite3ext.h"))
        zip.write(os.path.join(resultsPath, "sqlite3.c"), os.path.join("src", "sqlite3.c"))


def getZipPath(destLibDir):
    return os.path.join(destLibDir, f"{version}.zip")


def doesNeedBuilding():
    destLibDir = os.path.join(os.getcwd(), "lib")

    zipDir = getZipPath(destLibDir)

    isBuilt = os.path.exists(zipDir)

    return not isBuilt


def downloadBinaries():
    print("Trying to download pre-built binaries...")

    url = downloadURL

    if url == "":
        return False

    destLibDir = os.path.join(os.getcwd(), "lib")
    zipDir = getZipPath(destLibDir)

    result = downloadBinary(url, zipDir)

    print("Finished trying.")

    return result


def downloadBinary(url, outputPath):
    print(f"Trying to download url: '{url}' to path: '{outputPath}'")

    cmd = [curlPath, "--create-dirs", "-Lo", f"{outputPath}", f"{url}"]

    if runCmdIgnoreError(cmd):
        print(f"Downloaded binary: {url}")
        return True
    else:
        print(f"Failed to download binary: {url}")
        return False


print(f"Building sqlite3 version {version}...")

args = configureArguments()

cwd = os.getcwd()
tempDirPath = os.path.join(cwd, "__temp")

if doesNeedBuilding():
    if downloadBinaries():
        print("Downloaded pre-built binaries.")
    else:
        build(tempDirPath)

        saveResults(tempDirPath)
else:
    print("sqlite3 is already built...")

print(f"Built sqlite3 version {version}.")