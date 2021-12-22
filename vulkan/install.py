import os
import shutil
import platform
import argparse
import subprocess
import zipfile

version = "1.2.198.1"
installerExtension = "exe"

curlPath = shutil.which("curl")

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
    installDir = os.path.join(path, "vulkan", platform.system())

    return installDir


def isAlreadyInstalled(path):
    installDir = getFullInstallDir(path)

    filesExist = os.path.exists(installDir)

    return filesExist


def performInstall(tempDirPath, installPath):
    if platform.system() == "Windows":
        return
    elif platform.system() == "Darwin":
        hdiutilPath = shutil.which("hdiutil")

        # opens the cmd into `/Volumes/`
        cmd = [hdiutilPath, "attach", f"{tempDirPath}/vulkan_sdk.dmg"]
        runCmd(cmd)

        # from https://vulkan.lunarg.com/issue/view/61bca04a5df1129bc631eb3c
        cmd = [f"/Volumes/vulkansdk-macos-{version}/InstallVulkan.app/Contents/MacOS/InstallVulkan",
                "in",
                "-c",
                "--al",
                "-t",
                f"{installPath}",
                f"copy_only=1"]
        runCmd(cmd)

        cmd = [hdiutilPath, "detach", f"/Volumes/vulkansdk-macos-{version}/"]
        runCmd(cmd)
    else: # linux
        return


def install(path):
    cwd = os.getcwd()

    # download the installer
    tempDirPath = os.path.join(cwd, "__temp")
    createDirectories(tempDirPath)

    os.chdir(tempDirPath)

    installerExtension = "exe"
    platformName = "windows"

    if platform.system() == "Darwin":
        installerExtension = "dmg"
        platformName = "mac"
    elif platform.system() == "Linux":
        installerExtension = "tar.gz"
        platformName = "linux"

    cmd = [curlPath, "-LO", f"https://sdk.lunarg.com/sdk/download/{version}/{platformName}/vulkan_sdk.{installerExtension}"]
    runCmd(cmd)

    installDir = getFullInstallDir(path)

    performInstall(tempDirPath, installDir)

    os.chdir(cwd)


print("Installing Vulkan SDK...")

args = configureArguments()

if args.version is not None and len(args.version) > 0:
    version = args.version

if isAlreadyInstalled(args.path):
    print("Vulkan SDK already installed.")
else:
    install(args.path)

print("Installed Vulkan SDK.")
