import os
import shutil
import platform
import argparse
import subprocess

version = "v0.9.0-pre16"
gitURL = "https://github.com/HappySeaFox/sail.git"

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

    installPath = getInstallPath(tempDirPath)
    createDirectories(installPath)

    # get the latest code
    cmd = [gitPath, "clone", f"{gitURL}"]
    runCmd(cmd)

    os.chdir(os.path.join(os.getcwd(), "sail"))

    # checkout the version we want
    cmd = [gitPath, "checkout", f"tags/{version}", "-b", f"{version}"]
    runCmd(cmd)

    # build with cmake
    buildDir = os.path.join(os.getcwd(), "build")
    createDirectories(buildDir)
    os.chdir(buildDir)

    cmd = [cmakePath, "..", "-DSAIL_STATIC=ON", f"-DCMAKE_INSTALL_PREFIX={installPath}"]

    # apple clang doesn't seem to recognize C11, so use
    # clang installed with homebrew
    if platform.system() == "Darwin":
        cmd += ["-DCMAKE_C_COMPILER=/usr/local/opt/llvm/bin/clang"]

    runCmd(cmd)

    cmd = [cmakePath, "--build", ".", "--config", "Release"]
    runCmd(cmd)

    # save output into install folder
    cmd = [cmakePath, "--install", ".", "--config", "Release"]
    runCmd(cmd)

    os.chdir(cwd)

    print("Finished build.")


def saveResults(tempDirPath):
    print("Saving results...")

    installPath = getInstallPath(tempDirPath)
    
    destLibDir = os.path.join(os.getcwd(), "lib", platform.system())
    createDirectories(destLibDir)

    zipDir = getZipPath(destLibDir)

    shutil.make_archive(zipDir, "zip", installPath)
    
    print("Saved results.")


def getInstallPath(tempDirPath):
    return os.path.join(tempDirPath, "install")


def getZipPath(destLibDir):
    return os.path.join(destLibDir, f"{version}_{platform.system()}")


def doesNeedBuilding():
    destLibDir = os.path.join(os.getcwd(), "lib", platform.system())

    zipDir = getZipPath(destLibDir) + ".zip"

    isBuilt = os.path.exists(zipDir)

    return not isBuilt


def tryAndDownloadBinaries():
    print("Trying to download pre-built binaries...")

    downloadURLWindows = f""
    downloadURLDarwin = f""
    downloadURLLinux = f""

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

    destLibDir = os.path.join(os.getcwd(), "lib", platform.system())
    zipDir = getZipPath(destLibDir, platform.system())

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


print(f"Building SAIL version {version}...")

args = configureArguments()

if args.version is not None and len(args.version) > 0:
    version = args.version

cwd = os.getcwd()
tempDirPath = os.path.join(cwd, "__temp")

if doesNeedBuilding():
    if tryAndDownloadBinaries():
        print("Downloaded pre-built binaries.")
    else:
        build(tempDirPath)

        saveResults(tempDirPath)
else:
    print("SAIL is already built...")

print(f"Built SAIL version {version}.")