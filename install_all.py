import os
import shutil
import platform
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

    cmd = [f"{pythonPath}", f"{buildPath}"]
    runCmd(cmd)

    cmd = [f"{pythonPath}", f"{installPath}", "-p", path]
    runCmd(cmd)

    # if platform.system() == "Darwin":
        # # iOS
        # cmd = [f"{pythonPath}", f"{buildPath}", "-ios"]
        # runCmd(cmd)

        # cmd = [f"{pythonPath}", f"{installPath}", "-p", path, "-ios"]
        # runCmd(cmd)

        # # iOS Simulator
        # cmd = [f"{pythonPath}", f"{buildPath}", "-iossim"]
        # runCmd(cmd)

        # cmd = [f"{pythonPath}", f"{installPath}", "-p", path, "-iossim"]
        # runCmd(cmd)

    os.chdir(cwd)

    print("Installed v8.")


def installSDL(path):
    print("Installing SDL...")

    cwd = os.getcwd()
    os.chdir("sdl")

    buildPath = os.path.join(os.getcwd(), "build.py")
    installPath = os.path.join(os.getcwd(), "install.py")

    # build standard
    cmd = [f"{pythonPath}", f"{buildPath}"]
    runCmd(cmd)

    # build ios
    if platform.system() == "Darwin":
        cmd = [f"{pythonPath}", f"{buildPath}", "-ios"]
        runCmd(cmd)

    # install standard
    cmd = [f"{pythonPath}", f"{installPath}", "-p", f"{path}"]
    runCmd(cmd)

    # install ios
    if platform.system() == "Darwin":
        cmd = [f"{pythonPath}", f"{installPath}", "-p", f"{path}", "-ios"]
        runCmd(cmd)

        cmd = [f"{pythonPath}", f"{installPath}", "-p", f"{path}", "-iossim"]
        runCmd(cmd)

    os.chdir(cwd)

    print("Installed SDL.")


def installSDLimage(path):
    print("Installing SDL image...")

    cwd = os.getcwd()
    os.chdir("sdl_image")

    buildPath = os.path.join(os.getcwd(), "build.py")
    installPath = os.path.join(os.getcwd(), "install.py")

    # build standard
    cmd = [f"{pythonPath}", f"{buildPath}"]
    runCmd(cmd)

    # build ios
    if platform.system() == "Darwin":
        cmd = [f"{pythonPath}", f"{buildPath}", "-ios"]
        runCmd(cmd)

    # install standard
    cmd = [f"{pythonPath}", f"{installPath}", "-p", f"{path}"]
    runCmd(cmd)

    # install ios
    if platform.system() == "Darwin":
        cmd = [f"{pythonPath}", f"{installPath}", "-p", f"{path}", "-ios"]
        runCmd(cmd)

        cmd = [f"{pythonPath}", f"{installPath}", "-p", f"{path}", "-iossim"]
        runCmd(cmd)

    os.chdir(cwd)

    print("Installed SDL image.")


def installSDLnet(path):
    print("Installing SDL net...")

    cwd = os.getcwd()
    os.chdir("sdl_net")

    buildPath = os.path.join(os.getcwd(), "build.py")
    installPath = os.path.join(os.getcwd(), "install.py")

    # build standard
    cmd = [f"{pythonPath}", f"{buildPath}"]
    runCmd(cmd)

    # # build ios
    # if platform.system() == "Darwin":
    #     cmd = [f"{pythonPath}", f"{buildPath}", "-ios"]
    #     runCmd(cmd)

    # install standard
    cmd = [f"{pythonPath}", f"{installPath}", "-p", f"{path}"]
    runCmd(cmd)

    # # install ios
    # if platform.system() == "Darwin":
    #     cmd = [f"{pythonPath}", f"{installPath}", "-p", f"{path}", "-ios"]
    #     runCmd(cmd)

    #     cmd = [f"{pythonPath}", f"{installPath}", "-p", f"{path}", "-iossim"]
    #     runCmd(cmd)

    os.chdir(cwd)

    print("Installed SDL net.")


def installSDLttf(path):
    print("Installing SDL ttf...")

    cwd = os.getcwd()
    os.chdir("sdl_ttf")

    buildPath = os.path.join(os.getcwd(), "build.py")
    installPath = os.path.join(os.getcwd(), "install.py")

    # build standard
    cmd = [f"{pythonPath}", f"{buildPath}"]
    runCmd(cmd)

    # # build ios
    # if platform.system() == "Darwin":
    #     cmd = [f"{pythonPath}", f"{buildPath}", "-ios"]
    #     runCmd(cmd)

    # install standard
    cmd = [f"{pythonPath}", f"{installPath}", "-p", f"{path}"]
    runCmd(cmd)

    # # install ios
    # if platform.system() == "Darwin":
    #     cmd = [f"{pythonPath}", f"{installPath}", "-p", f"{path}", "-ios"]
    #     runCmd(cmd)

    #     cmd = [f"{pythonPath}", f"{installPath}", "-p", f"{path}", "-iossim"]
    #     runCmd(cmd)

    os.chdir(cwd)

    print("Installed SDL ttf.")


def installSDLmixer(path):
    print("Installing SDL mixer...")

    cwd = os.getcwd()
    os.chdir("sdl_mixer")

    buildPath = os.path.join(os.getcwd(), "build.py")
    installPath = os.path.join(os.getcwd(), "install.py")

    # build standard
    cmd = [f"{pythonPath}", f"{buildPath}"]
    runCmd(cmd)

    # # build ios
    # if platform.system() == "Darwin":
    #     cmd = [f"{pythonPath}", f"{buildPath}", "-ios"]
    #     runCmd(cmd)

    # install standard
    cmd = [f"{pythonPath}", f"{installPath}", "-p", f"{path}"]
    runCmd(cmd)

    # # install ios
    # if platform.system() == "Darwin":
    #     cmd = [f"{pythonPath}", f"{installPath}", "-p", f"{path}", "-ios"]
    #     runCmd(cmd)

    #     cmd = [f"{pythonPath}", f"{installPath}", "-p", f"{path}", "-iossim"]
    #     runCmd(cmd)

    os.chdir(cwd)

    print("Installed SDL mixer.")


print("Installing all dependencies...")

args = configureArguments()

installPath = os.path.join(args.path, "libraries")

installClang(installPath)

installv8(installPath)

installSDL(installPath)

installSDLimage(installPath)

installSDLnet(installPath)

installSDLttf(installPath)

installSDLmixer(installPath)

print("Installed all dependencies.")