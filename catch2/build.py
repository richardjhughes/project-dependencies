import os
import shutil
import platform
import argparse
import subprocess
import zipfile

version = "2.13.6"
gitUrl = "https://github.com/catchorg/Catch2.git"

downloadURL = ""

gitPath = shutil.which("git")
curlPath = shutil.which("curl")
cmakePath = shutil.which("cmake")

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

    cmd = [cmakePath, "--build", ".", "--config", "Release"]
    runCmd(cmd)

    cmd = [cmakePath, "--install", ".", "--config", "Release"]
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

    includePrefix = os.path.join("include", "catch2")
    includeDir = os.path.join(resultsPath, includePrefix)

    libPrefix = os.path.join("lib", "cmake", "Catch2")
    libDir = os.path.join(resultsPath, libPrefix)

    with zipfile.ZipFile(zipDir, "w") as zip:
        zip.write(os.path.join(includeDir, "catch.hpp"), os.path.join(includePrefix, "catch.hpp"))
        zip.write(os.path.join(includeDir, "catch_reporter_automake.hpp"), os.path.join(includePrefix, "catch_reporter_automake.hpp"))
        zip.write(os.path.join(includeDir, "catch_reporter_sonarqube.hpp"), os.path.join(includePrefix, "catch_reporter_sonarqube.hpp"))
        zip.write(os.path.join(includeDir, "catch_reporter_tap.hpp"), os.path.join(includePrefix, "catch_reporter_tap.hpp"))
        zip.write(os.path.join(includeDir, "catch_reporter_teamcity.hpp"), os.path.join(includePrefix, "catch_reporter_teamcity.hpp"))

        zip.write(os.path.join(libDir, "Catch.cmake"), os.path.join(libPrefix, "Catch.cmake"))
        zip.write(os.path.join(libDir, "Catch2Config.cmake"), os.path.join(libPrefix, "Catch2Config.cmake"))
        zip.write(os.path.join(libDir, "Catch2ConfigVersion.cmake"), os.path.join(libPrefix, "Catch2ConfigVersion.cmake"))
        zip.write(os.path.join(libDir, "Catch2Targets.cmake"), os.path.join(libPrefix, "Catch2Targets.cmake"))
        zip.write(os.path.join(libDir, "CatchAddTests.cmake"), os.path.join(libPrefix, "CatchAddTests.cmake"))
        zip.write(os.path.join(libDir, "ParseAndAddCatchTests.cmake"), os.path.join(libPrefix, "ParseAndAddCatchTests.cmake"))


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


print(f"Building catch2 version {version}...")

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
    print("catch2 is already built...")

print(f"Built catch2 version {version}.")