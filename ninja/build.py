import os
import shutil
import platform
import argparse
import subprocess

version = "1.11.1"

gitPath = shutil.which("git")
cmakePath = shutil.which("cmake")
curlPath = shutil.which("curl")

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


def getZipPath(destLibDir, platformLibName):
    return os.path.join(destLibDir, f"{version}_{platformLibName}.zip")


def doesNeedBuilding():
    platformLibName = platform.system()

    destLibDir = os.path.join(os.getcwd(), "lib", platformLibName)

    zipDir = getZipPath(destLibDir, platformLibName)

    isBuilt = os.path.exists(zipDir)

    return not isBuilt


def downloadBinaries():
    print("Trying to download pre-built binaries...")

    # we will just download the prebuilt releases from github
    downloadURLWindows = f"https://github.com/ninja-build/ninja/releases/download/v{version}/ninja-win.zip"
    downloadURLDarwin = f"https://github.com/ninja-build/ninja/releases/download/v{version}/ninja-mac.zip"
    downloadURLLinux = f"https://github.com/ninja-build/ninja/releases/download/v{version}/ninja-linux.zip"

    url = ""

    system_name = platform.system()
    if system_name == "Windows":
        url = downloadURLWindows
    elif system_name == "Darwin":
        url = downloadURLDarwin
    elif system_name == "Linux":
        url = downloadURLLinux
    else:
        print(f"Unknown system name: {system_name}")
        return False

    if url == "":
        return False

    platformLibName = platform.system()

    destLibDir = os.path.join(os.getcwd(), "lib", platformLibName)
    zipDir = getZipPath(destLibDir, platformLibName)

    result = downloadBinary(url, zipDir)

    print("Finished trying.")

    return result


def downloadBinary(url, output_path):
    print(f"Trying to download url: '{url}' to path: '{output_path}'")

    cmd = [curlPath, "--create-dirs", "-Lo", f"{output_path}", f"{url}"]

    if runCmdIgnoreError(cmd):
        print(f"Downloaded binary: {url}")
        return True
    else:
        print(f"Failed to download binary: {url}")
        return False


print(f"Building Ninja version {version}...")

args = configureArguments()

if args.version is not None and len(args.version) > 0:
    version = args.version

cwd = os.getcwd()
tempDirPath = os.path.join(cwd, "__temp")

if doesNeedBuilding():
    if downloadBinaries():
        print("Downloaded pre-built binaries.")
    else:
        print("Failed to download pre-build binaries.")
else:
    print("Ninja is already built...")

print(f"Built Ninja version {version}.")