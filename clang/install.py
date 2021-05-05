import os
import shutil
import platform
import argparse
import subprocess
import zipfile

def configureArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", action="store", required=True, help="path to install in")
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


def install(path):
    print("Starting install...")

    installDir = getFullInstallDir(path)

    print(f"Installing in directory: {installDir}")

    createDirectories(installDir)

    osName = platform.system()

    if osName == "Windows":
        installForWindows(installDir)
    elif osName == "Darwin":
        installForDarwin(installDir)
    elif osName == "Linux":
        installForLinux(installDir)
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

    installDir = os.path.join(path, "clang-12", platformName)

    return installDir


def installForWindows(installDir):
    print("Installing for Windows...")

    tempDir = os.path.join(os.getcwd(), "__temp")

    createDirectories(tempDir)

    cwd = os.getcwd()
    os.chdir(tempDir)

    filename = "clang.zip"

    # download clang
    cmd = ["curl", "-L", "https://github.com/richardjhughes/project-dependencies/releases/download/LLVM_12.0.0/LLVM_12.0.0_Windows.zip", "-o", filename]
    runCmd(cmd)

    # install
    with zipfile.ZipFile(filename) as zip:
        zip.extractall(installDir)

    os.chdir(cwd)
    removeDirectory(tempDir)

    print("Installed for Windows.")


def installForDarwin(installDir):
    print("Installing for Darwin...")

    tempDir = os.path.join(os.getcwd(), "__temp")

    createDirectories(tempDir)

    cwd = os.getcwd()
    os.chdir(tempDir)

    filename = "clang.tar.xf"

    # download clang
    cmd = ["curl", "-L", "https://github.com/llvm/llvm-project/releases/download/llvmorg-12.0.0/clang+llvm-12.0.0-x86_64-apple-darwin.tar.xz", "-o", filename]
    runCmd(cmd)

    # install
    cmd = ["tar", "-C", f"{installDir}", "-xf", f"{filename}", "--strip-components", "1"]
    runCmd(cmd)

    os.chdir(cwd)
    removeDirectory(tempDir)

    print("Installed for Darwin.")


def installForLinux(installDir):
    print("Installing for Linux...")

    tempDir = os.path.join(os.getcwd(), "__temp")

    createDirectories(tempDir)

    cwd = os.getcwd()
    os.chdir(tempDir)

    filename = "clang.tar.xf"

    # download clang
    cmd = ["curl", "-L", "https://github.com/llvm/llvm-project/releases/download/llvmorg-12.0.0/clang+llvm-12.0.0-x86_64-linux-gnu-ubuntu-20.04.tar.xz", "-o", filename]
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
    install(args.path)

print("Installed clang.")