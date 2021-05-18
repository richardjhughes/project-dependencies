import os
import shutil
import platform
import argparse
import subprocess
import zipfile

version = "2.2.0"
gitUrl = "https://github.com/nigels-com/glew.git"

sdlDownloadURLWindows = ""
sdlDownloadURLDarwin = ""
sdlDownloadURLiOS = ""
sdlDownloadURLLinux = ""

gitPath = shutil.which("git")
curlPath = shutil.which("curl")
cmakePath = shutil.which("cmake")

def configureArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-ios", "--ios", action="store_true", required=False, help="Build iOS and iOS Simulator universal binaries. Note: Only valid for use when building on MacOS")
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


def build(buildiOS, tempDirPath):
    print("Starting build...")

    if platform.system() != "Darwin" and buildiOS:
        print("Can only build iOS on MacOS.")
        return

    if platform.system() == "Windows":
        print("Please build manually on Windows.")
        return

    createDirectories(tempDirPath)

    os.chdir(tempDirPath)

    # get the latest code
    cmd = [gitPath, "clone", f"{gitUrl}"]
    runCmd(cmd)

    sourceDir = os.path.join(os.getcwd(), "glew")
    os.chdir(sourceDir)

    # checkout the version we want
    cmd = [gitPath, "checkout", f"tags/glew-{version}", "-b", f"glew-{version}"]
    runCmd(cmd)

    cmakeDir = os.path.join(sourceDir, "build", "cmake")
    os.chdir(cmakeDir)

    buildDir = os.path.join(cmakeDir, "build")
    createDirectories(buildDir)

    os.chdir(buildDir)

    cmd = [cmakePath, ".."]
    runCmd(cmd)

    cmd = [cmakePath, "--build", ".", "--config", "Release"]
    runCmd(cmd)

    os.chdir(cwd)

    print("Finished build.")


def saveResults(buildiOS, tempDirPath):
    if platform.system() == "Windows":
        # building on Windows is manual
        return

    print("Saving results...")

    outputFolder = ""

    if platform.system() == "Darwin":
        if buildiOS:
            outputFolder = "libsodium-ios"
        else:
            outputFolder = "libsodium-osx"
    elif platform.system() == "Linux":
        outputFolder = "libsodium-linux"

    resultsPath = os.path.join(tempDirPath, "libsodium", outputFolder)

    platformLibName = getPlatformLibName(buildiOS)

    destLibDir = os.path.join(os.getcwd(), "lib", platformLibName)

    saveBinaries(destLibDir, platformLibName, resultsPath)

    print("Saved results.")


def saveBinaries(destLibDir, platformLibName, resultsPath):
    createDirectories(destLibDir)

    resultsLibDir = os.path.join(resultsPath, "lib")
    resultsIncludeDir = os.path.join(resultsPath, "include")
    resultsIncludesDir = os.path.join(resultsIncludeDir, "sodium")

    zipDir = getZipPath(destLibDir, platformLibName)

    with zipfile.ZipFile(zipDir, "w") as zip:
        for root, dirs, files in os.walk(resultsLibDir):
            for file in files:
                zip.write(os.path.join(root, file), os.path.join("lib", file))

        zip.write(os.path.join(resultsIncludeDir, "sodium.h"), os.path.join("include", "sodium.h"))

        for root, dirs, files in os.walk(resultsIncludesDir):
            for file in files:
                zip.write(os.path.join(root, file), os.path.join("include", "sodium", file))


def getPlatformLibName(buildiOS):
    if platform.system() == "Darwin":
        if buildiOS:
            return "iOS"

    return platform.system()


def getZipPath(destLibDir, platformLibName):
    return os.path.join(destLibDir, f"{version}_{platformLibName}.zip")


def doesNeedBuilding(buildiOS):
    platformLibName = getPlatformLibName(buildiOS)

    destLibDir = os.path.join(os.getcwd(), "lib", platformLibName)

    zipDir = getZipPath(destLibDir, platformLibName)

    isBuilt = os.path.exists(zipDir)

    return not isBuilt


def tryAndDownloadBinaries(buildiOS):
    
    # as we build both ios and ios simulator together, try and
    # download them together
    if platform.system() == "Darwin":
        result = downloadBinaries(buildiOS)
        return result
    else:
        result = downloadBinaries(False)
        return result


def downloadBinaries(buildiOS):
    print("Trying to download pre-built binaries...")

    url = ""

    systemName = platform.system()
    if systemName == "Windows":
        url = sdlDownloadURLWindows
    elif systemName == "Darwin":
        if buildiOS:
            url = sdlDownloadURLiOS
        else:
            url = sdlDownloadURLDarwin
    elif systemName == "Linux":
        url = sdlDownloadURLLinux
    else:
        print(f"Unknown system name: {systemName}")
        return False

    if url == "":
        return False

    platformLibName = getPlatformLibName(buildiOS)

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

# if doesNeedBuilding(args.ios):
#     if tryAndDownloadBinaries(args.ios):
#         print("Downloaded pre-built binaries.")
#     else:
build(args.ios, tempDirPath)

#         saveResults(args.ios, tempDirPath)
# else:
#     print("glew is already built...")

print(f"Built glew version {version}.")