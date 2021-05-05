import os
import shutil
import argparse
import subprocess

pythonPath = shutil.which("python3")

def configureArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", action="store", required=True, help="path to project")
    args = parser.parse_args()

    return args


def runCmd(cmd, cwd=None):
    print(f"Running command: {cmd}")
    subprocess.run(cmd, cwd=cwd)


def installClang(path):
    print("Installing clang...")

    installPath = os.path.join(os.getcwd(), "clang", "install.py")

    cmd = [f"{pythonPath}", f"{installPath}", "-p", path]
    runCmd(cmd)

    print("Installed clang.")


def installv8(path):
    print("Installing v8...")

    cwd = os.getcwd()
    os.chdir("v8")

    buildPath = os.path.join(os.getcwd(), "build.py")
    installPath = os.path.join(os.getcwd(), "install.py")

    # Standard MacOS
    cmd = [f"{pythonPath}", f"{buildPath}"]
    runCmd(cmd)

    cmd = [f"{pythonPath}", f"{installPath}", "-p", path]
    runCmd(cmd)

    # # iOS
    # cmd = [f"{pythonPath}", f"{buildPath}", "-ios"]
    # runCmd(cmd)

    # cmd = [f"{pythonPath}", f"{installPath}", "-p", path, "-ios"]
    # runCmd(cmd)

    # iOS Simulator
    cmd = [f"{pythonPath}", f"{buildPath}", "-iossim"]
    runCmd(cmd)

    cmd = [f"{pythonPath}", f"{installPath}", "-p", path, "-iossim"]
    runCmd(cmd)

    os.chdir(cwd)

    print("Installed v8.")


print("Installing all dependencies...")

args = configureArguments()

installPath = os.path.join(args.path, "libraries")

installClang(installPath)
installv8(installPath)

print("Installed all dependencies.")