import os
import shutil
import platform
import argparse
import zipfile

sdlVersion = "1.0.18"

def configureArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", action="store", required=True, help="path to install in")
    parser.add_argument("-ios", "--ios", action="store_true", required=False, help="Install iOS and iOS Simulator universal binaries. Note: Only valid for use when building on MacOS")
    args = parser.parse_args()

    return args


def createDirectories(path):
    print(f"Creating directory: {path}")

    try:
        os.makedirs(path)
    except OSError as error:
        print(error)


def getFullInstallDir(path, buildForiOS):
    osName = platform.system()

    platformName = ""

    if osName == "Windows":
        platformName = "windows"
    elif osName == "Darwin":
        if buildForiOS:
            platformName = "ios"
        else:
            platformName = "darwin"
    elif osName == "Linux":
        platformName = "linux"
    else:
        platformName = "unknown"

    installDir = os.path.join(path, "libsodium", platformName)

    return installDir


def isSDLAlreadyInstalled(path, buildForiOS):
    installDir = getFullInstallDir(path, buildForiOS)

    filesExist = False

    if platform.system() == "Windows":
        filesExist = (os.path.exists(os.path.join(installDir, "lib", "libsodium.lib")) and
                      os.path.exists(os.path.join(installDir, "include")))
    elif platform.system() == "Linux":
        filesExist = (os.path.exists(os.path.join(installDir, "lib", "libsodium.a")) and
                      os.path.exists(os.path.join(installDir, "lib", "libsodium.la")) and
                      os.path.exists(os.path.join(installDir, "lib", "libsodium.so")) and
                      os.path.exists(os.path.join(installDir, "include")))
    else:
        filesExist = (os.path.exists(os.path.join(installDir, "lib", "libsodium.a")) and
                      os.path.exists(os.path.join(installDir, "lib", "libsodium.dylib")) and
                      os.path.exists(os.path.join(installDir, "include")))

    return filesExist


def getPlatformName(buildForiOS):
    platformName = platform.system()

    if buildForiOS:
        platformName = "iOS"

    return platformName


def getBinaryOutPath(buildForiOS):
    platformName = getPlatformName(buildForiOS)

    binaryOut = os.path.join(os.getcwd(), "lib", platformName)

    return binaryOut


def getOutputZipPath(binaryOutPath, buildForiOS):
    platformName = getPlatformName(buildForiOS)

    zipPath = os.path.join(binaryOutPath, f"{sdlVersion}_{platformName}.zip")

    return zipPath


def install(path, buildForiOS):
    binaryPath = getBinaryOutPath(buildForiOS)
    zipPath = getOutputZipPath(binaryPath, buildForiOS)

    installDir = getFullInstallDir(path, buildForiOS)

    createDirectories(installDir)

    with zipfile.ZipFile(zipPath, "r") as zip:
        zip.extractall(installDir)


print("Installing libSodium...")

args = configureArguments()

if isSDLAlreadyInstalled(args.path, args.ios):
    print("libSodium already installed.")
else:
    install(args.path, args.ios)

print("Installed libSodium.")
