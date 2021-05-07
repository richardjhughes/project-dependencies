import os
import shutil
import platform
import argparse
import zipfile

sdlVersion = "2.0.14"

def configureArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", action="store", required=True, help="path to install in")
    parser.add_argument("-ios", "--ios", action="store_true", default=False, help="Install for iOS. Note: Only valid for use when building on MacOS")
    parser.add_argument("-iossim", "--ios-simulator", action="store_true", default=False, help="Install for iOS simulator. Note: Only valid for use when building on MacOS")
    args = parser.parse_args()

    return args


def createDirectories(path):
    print(f"Creating directory: {path}")

    try:
        os.makedirs(path)
    except OSError as error:
        print(error)


def getFullInstallDir(path, buildForiOS, buildForiOSSimulator):
    osName = platform.system()

    platformName = ""

    if osName == "Windows":
        platformName = "windows"
    elif osName == "Darwin":
        if buildForiOS:
            platformName = "ios"
        elif buildForiOSSimulator:
            platformName = "ios_simulator"
        else:
            platformName = "darwin"
    elif osName == "Linux":
        platformName = "linux"
    else:
        platformName = "unknown"

    installDir = os.path.join(path, "sdl", platformName)

    return installDir


def isSDLAlreadyInstalled(path, buildForiOS, buildForiOSSimulator):
    installDir = getFullInstallDir(path, buildForiOS, buildForiOSSimulator)

    filesExist = ((os.path.exists(os.path.join(installDir, "sdl.a")) or os.path.exists(os.path.join(installDir, "sdl.lib"))) and
                  (os.path.exists(os.path.join(path, "sdl", "include"))))

    return filesExist


def getBinaryOutPath(buildForiOS, buildForiOSSimulator):
    platformName = platform.system()

    if buildForiOS:
        platformName = "iOS"
    elif buildForiOSSimulator:
        platformName = "iOS_Simulator"

    binaryOut = os.path.join(os.getcwd(), "lib", platformName)

    return binaryOut


def getOutputZipPath(binaryOutPath):
    zipPath = os.path.join(binaryOutPath, f"sdl_{sdlVersion}.zip")

    return zipPath


def install(path, buildForiOS, buildForiOSSimulator):
    binaryPath = getBinaryOutPath(buildForiOS, buildForiOSSimulator)
    zipPath = getOutputZipPath(binaryPath)

    installDir = getFullInstallDir(path, buildForiOS, buildForiOSSimulator)

    createDirectories(installDir)

    with zipfile.ZipFile(zipPath, "r") as zip:
        zip.extractall(installDir)

    shutil.copytree(os.path.join(os.getcwd(), "include"), os.path.join(path, "sdl", "include"))

print("Installing SDL...")

args = configureArguments()

if isSDLAlreadyInstalled(args.path, args.ios, args.ios_simulator):
    print("SDL already installed.")
else:
    install(args.path, args.ios, args.ios_simulator)

print("Installed SDL.")