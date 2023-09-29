import os
import glob
import shutil
import platform
import argparse
import subprocess
import zipfile

version = "3.4.0"
gitUrl = "https://github.com/catchorg/Catch2.git"

gitPath = shutil.which("git")
curlPath = shutil.which("curl")
cmakePath = shutil.which("cmake")

def configureArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action="store", required=False, help="version to install")
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

    createDirectories(tempDirPath)

    os.chdir(tempDirPath)

    # get the latest code
    cmd = [gitPath, "clone", f"{gitUrl}"]
    runCmd(cmd)

    os.chdir(os.path.join(tempDirPath, "Catch2"))

    # checkout the version we want
    cmd = [gitPath, "checkout", f"tags/v{version}", "-b", f"v{version}"]
    runCmd(cmd)

    installDir = os.path.join(os.getcwd(), "__install")

    buildDir = os.path.join(os.getcwd(), "build")
    createDirectories(buildDir)
    os.chdir(buildDir)

    # build
    cmd = [cmakePath, f"-DCMAKE_INSTALL_PREFIX={installDir}", ".."]
    runCmd(cmd)

    cmd = [cmakePath, "--build", "."]
    runCmd(cmd)

    cmd = [cmakePath, "--install", "."]
    runCmd(cmd)

    os.chdir(cwd)

    print("Finished build.")


def saveResults(tempDirPath):
    print("Saving results...")

    resultsPath = os.path.join(tempDirPath, "Catch2", "__install")

    destLibDir = os.path.join(os.getcwd(), "lib")

    saveBinaries(destLibDir, resultsPath)

    print("Saved results.")


def saveBinaries(destLibDir, resultsPath):
    createDirectories(destLibDir)

    zipDir = getZipPath(destLibDir)

    with zipfile.ZipFile(zipDir, "w") as zip:
        for file in glob.glob(os.path.join(resultsPath, "**/*"), recursive=True):
            relativePath = file.replace(resultsPath, "")
            print(resultsPath)
            print(relativePath)
            print(file)
            zip.write(file, relativePath)


def getZipPath(destLibDir):
    return os.path.join(destLibDir, f"{version}.zip")


def doesNeedBuilding():
    destLibDir = os.path.join(os.getcwd(), "lib")

    zipDir = getZipPath(destLibDir)

    isBuilt = os.path.exists(zipDir)

    return not isBuilt


def downloadBinaries():
    print("Trying to download pre-built binaries...")

    downloadURL = f"https://github.com/snowmeltarcade/project-dependencies/releases/download/catch2_{version}/{version}.zip"

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


print(f"Building catch2 version {version}...")

args = configureArguments()

if args.version is not None and len(args.version) > 0:
    version = args.version

cwd = os.getcwd()
tempDirPath = os.path.join(cwd, "__temp")

if doesNeedBuilding():
    if downloadBinaries():
        print("Downloaded pre-built binaries.")
    else:
        build(tempDirPath)

        saveResults(tempDirPath)
else:
    print("catch2 is already built...")

print(f"Built catch2 version {version}.")