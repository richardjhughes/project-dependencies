import os
import shutil
import platform
import argparse
import zipfile

version = "2.2.0"

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

    installDir = os.path.join(path, "glew", platformName)

    return installDir


def isAlreadyInstalled(path):
    installDir = getFullInstallDir(path)

    filesExist = False

    if platform.system() == "Windows":
        filesExist = (os.path.exists(os.path.join(installDir, "lib", "glew32.lib")) and
                      os.path.exists(os.path.join(installDir, "lib", "libglew32.lib")) and
                      os.path.exists(os.path.join(installDir, "bin", "glew32.dll")) and
                      os.path.exists(os.path.join(installDir, "include", "GL")))
    elif platform.system() == "Darwin":
        filesExist = (os.path.exists(os.path.join(installDir, "lib", "libGLEW.a")) and
                      os.path.exists(os.path.join(installDir, "lib", "libGLEW.dylib")) and
                      os.path.exists(os.path.join(installDir, "include", "GL")))
    else:
        filesExist = (os.path.exists(os.path.join(installDir, "lib", "libGLEW.a")) and
                      os.path.exists(os.path.join(installDir, "lib", "libGLEW.so")) and
                      os.path.exists(os.path.join(installDir, "include", "GL")))

    return filesExist


def getPlatformName():
    platformName = platform.system()
    return platformName


def getBinaryOutPath():
    platformName = getPlatformName()

    binaryOut = os.path.join(os.getcwd(), "lib", platformName)

    return binaryOut


def getOutputZipPath(binaryOutPath):
    platformName = getPlatformName()

    zipPath = os.path.join(binaryOutPath, f"{version}_{platformName}.zip")

    return zipPath


def install(path):
    binaryPath = getBinaryOutPath()
    zipPath = getOutputZipPath(binaryPath)

    installDir = getFullInstallDir(path)

    createDirectories(installDir)

    with zipfile.ZipFile(zipPath, "r") as zip:
        zip.extractall(installDir)


print("Installing GLEW...")

args = configureArguments()

if args.version is not None and len(args.version) > 0:
    version = args.version

if isAlreadyInstalled(args.path):
    print("GLEW already installed.")
else:
    install(args.path)

print("Installed GLEW.")