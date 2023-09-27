import os
import shutil
import platform
import argparse
import subprocess
import zipfile

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


def removeDirectory(path):
    print(f"Removing directory: {path}")

    try:
        shutil.rmtree(path)
    except OSError as error:
        print(error)


def runCmd(cmd, cwd=None):
    print(f"Running command: {cmd}")
    subprocess.run(cmd, cwd=cwd)


def install(path, version):
    print("Starting install...")

    installDir = getFullInstallDir(path)

    print(f"Installing in directory: {installDir}")

    createDirectories(installDir)

    osName = platform.system()

    if version is None or len(version) <= 0:
        version = "17.0.1"

    if osName == "Windows":
        installForWindows(installDir, version)
    elif osName == "Darwin":
        installForDarwin(installDir, version)
    elif osName == "Linux":
        installForLinux(installDir, version)
    else:
        print("Unknown OS: " + osName)

    print("Finished install.")


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

    installDir = os.path.join(path, "clang", platformName)

    return installDir


def installForWindows(installDir, version):
    print("Installing for Windows...")

    tempDir = os.path.join(os.getcwd(), "__temp")

    createDirectories(tempDir)

    cwd = os.getcwd()
    os.chdir(tempDir)

    filename = "clang.zip"

    # download clang
    cmd = ["curl", "-L", f"https://github.com/richardjhughes/project-dependencies/releases/download/LLVM_{version}/LLVM_{version}_Windows.zip", "-o", filename]
    runCmd(cmd)

    # install
    with zipfile.ZipFile(filename) as zip:
        zip.extractall(installDir)

    os.chdir(cwd)
    removeDirectory(tempDir)

    print("Installed for Windows.")


def installForDarwin(installDir, version):
    print("Installing for Darwin...")

    tempDir = os.path.join(os.getcwd(), "__temp")

    createDirectories(tempDir)

    cwd = os.getcwd()
    os.chdir(tempDir)

    filename = "clang.tar.xf"

    # download clang
    cmd = ["curl", "-L", f"https://github.com/llvm/llvm-project/releases/download/llvmorg-{version}/clang+llvm-{version}-arm64-apple-darwin22.0.tar.xz", "-o", filename]
    runCmd(cmd)

    # install
    cmd = ["tar", "-C", f"{installDir}", "-xf", f"{filename}", "--strip-components", "1"]
    runCmd(cmd)

    os.chdir(cwd)
    removeDirectory(tempDir)

    print("Installed for Darwin.")


def installForLinux(installDir, version):
    print("Installing for Linux...")

    tempDir = os.path.join(os.getcwd(), "__temp")

    createDirectories(tempDir)

    cwd = os.getcwd()
    os.chdir(tempDir)

    filename = "clang.tar.xf"

    # download clang
    cmd = ["curl", "-L", f"https://github.com/llvm/llvm-project/releases/download/llvmorg-{version}/clang+llvm-{version}-x86_64-linux-gnu-ubuntu-20.04.tar.xz", "-o", filename]
    runCmd(cmd)

    # install
    cmd = ["tar", "-C", f"{installDir}", "-xf", f"{filename}", "--strip-components", "1"]
    runCmd(cmd)

    os.chdir(cwd)
    removeDirectory(tempDir)

    print("Installed for Linux.")


def isClangAlreadyInstalled(path):
    clangPath = os.path.join(getFullInstallDir(path), "bin", "clang-cl.exe" if platform.system() == "Windows" else "clang")

    if os.path.exists(clangPath):
        return True
    else:
        return False


print("Installing clang...")

args = configureArguments()

if isClangAlreadyInstalled(args.path):
    print("Clang already installed.")
else:
    install(args.path, args.version)

print("Installed clang.")
