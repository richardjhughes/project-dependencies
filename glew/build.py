import os
import shutil
import platform
import argparse
import subprocess
import zipfile

version = "2.2.0"
# the git tree does not contain the generated source
# it is far simpler to build from the release package which does contain the
# generated source
gitUrl = "https://github.com/nigels-com/glew/releases/download/glew-2.2.0/glew-2.2.0.zip"

downloadURLWindows = ""
downloadURLDarwin = "https://github.com/snowmeltarcade/project-dependencies/releases/download/glew_2.2.0/2.2.0_Darwin.zip"
downloadURLLinux = ""

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


def getZipOutputPath(tempDirPath):
    path = os.path.join(tempDirPath, "glew_source")
    return path

def getBuildPath(zipOutputPath):
    path = os.path.join(zipOutputPath, f"glew-{version}", "build", "cmake", "build")
    return path


def build(tempDirPath):
    print("Starting build...")

    createDirectories(tempDirPath)

    os.chdir(tempDirPath)

    # get the code
    zipPath = os.path.join(tempDirPath, "glew.zip")
    cmd = [curlPath, "--create-dirs", "-Lo", f"{zipPath}", f"{gitUrl}"]
    runCmd(cmd)

    zipOutputPath = getZipOutputPath(tempDirPath)
    with zipfile.ZipFile(zipPath, "r") as zip:
        zip.extractall(zipOutputPath)

    os.chdir(zipOutputPath)

    buildDir = getBuildPath(zipOutputPath)
    createDirectories(buildDir)

    os.chdir(buildDir)

    cmd = [cmakePath, ".."]
    runCmd(cmd)

    cmd = [cmakePath, "--build", ".", "--config", "Release"]
    runCmd(cmd)

    os.chdir(cwd)

    print("Finished build.")


def saveResults(tempDirPath):
    print("Saving results...")

    zipOutputPath = getZipOutputPath(tempDirPath)
    buildDir = getBuildPath(zipOutputPath)

    platformLibName = getPlatformLibName()

    destLibDir = os.path.join(os.getcwd(), "lib", platformLibName)
    includeDir = os.path.join(tempDirPath, "glew_source", f"glew-{version}", "include", "GL")

    saveBinaries(destLibDir, platformLibName, buildDir, includeDir)

    print("Saved results.")


def saveBinaries(destLibDir, platformLibName, buildDir, includeDir):
    createDirectories(destLibDir)

    resultsLibDir = os.path.join(buildDir, "lib")
    resultsBinDir = os.path.join(buildDir, "bin")

    zipDir = getZipPath(destLibDir, platformLibName)

    with zipfile.ZipFile(zipDir, "w") as zip:
        for root, dirs, files in os.walk(resultsLibDir):
            for file in files:
                zip.write(os.path.join(root, file), os.path.join("lib", file))

        for root, dirs, files in os.walk(resultsBinDir):
            for file in files:
                zip.write(os.path.join(root, file), os.path.join("bin", file))

        for root, dirs, files in os.walk(includeDir):
            for file in files:
                zip.write(os.path.join(root, file), os.path.join("include", "GL", file))


def getPlatformLibName():
    return platform.system()


def getZipPath(destLibDir, platformLibName):
    return os.path.join(destLibDir, f"{version}_{platformLibName}.zip")


def doesNeedBuilding():
    platformLibName = getPlatformLibName()

    destLibDir = os.path.join(os.getcwd(), "lib", platformLibName)

    zipDir = getZipPath(destLibDir, platformLibName)

    isBuilt = os.path.exists(zipDir)

    return not isBuilt


def downloadBinaries():
    print("Trying to download pre-built binaries...")

    url = ""

    systemName = platform.system()
    if systemName == "Windows":
        url = downloadURLWindows
    elif systemName == "Darwin":
            url = downloadURLDarwin
    elif systemName == "Linux":
        url = downloadURLLinux
    else:
        print(f"Unknown system name: {systemName}")
        return False

    if url == "":
        return False

    platformLibName = getPlatformLibName()

    destLibDir = os.path.join(os.getcwd(), "lib", platformLibName)
    zipDir = getZipPath(destLibDir, platformLibName)

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


print(f"Building glew version {version}...")

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
    print("glew is already built...")

print(f"Built glew version {version}.")