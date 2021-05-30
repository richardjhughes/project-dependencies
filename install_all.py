import os
import json
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


def getProjectDependencies(path):
    print("Checking for project dependencies...")

    fileName = "libraries.json"
    filePath = os.path.join(path, fileName)

    if not os.path.exists(filePath) or not os.path.isfile(filePath):
        print(f"Failed to find `{fileName}`.")
        return {}

    dependencies = {}

    dependenciesFile = open(filePath)
    dependenciesJson = json.load(dependenciesFile)

    for d in dependenciesJson["dependencies"]:
        dependencies[d["name"]] = d["version"]

    dependenciesFile.close()

    print("Checked.")

    return dependencies


def installClang(path, deps):
    if len(deps) > 0 and not "clang" in deps.keys():
        return

    print("Installing clang...")

    version = []
    if len(deps) > 0:
        version = ["-v", f"{deps['clang']}"]

    installPath = os.path.join(os.getcwd(), "clang", "install.py")

    cmd = [f"{pythonPath}", f"{installPath}", "-p", path] + version
    runCmd(cmd)

    print("Installed clang.")


def installv8(path, deps):
    if len(deps) > 0 and not "v8" in deps.keys():
        return

    print("Installing v8...")

    version = []
    if len(deps) > 0:
        version = ["-v", f"{deps['v8']}"]

    cwd = os.getcwd()
    os.chdir("v8")

    buildPath = os.path.join(os.getcwd(), "build.py")
    installPath = os.path.join(os.getcwd(), "install.py")

    cmd = [f"{pythonPath}", f"{buildPath}"] + version
    runCmd(cmd)

    cmd = [f"{pythonPath}", f"{installPath}", "-p", path] + version
    runCmd(cmd)

    if platform.system() == "Darwin":
        # iOS
        cmd = [f"{pythonPath}", f"{buildPath}", "-ios"] + version
        runCmd(cmd)

        cmd = [f"{pythonPath}", f"{installPath}", "-p", path, "-ios"] + version
        runCmd(cmd)

        # iOS Simulator
        cmd = [f"{pythonPath}", f"{buildPath}", "-iossim"] + version
        runCmd(cmd)

        cmd = [f"{pythonPath}", f"{installPath}", "-p", path, "-iossim"] + version
        runCmd(cmd)

    os.chdir(cwd)

    print("Installed v8.")


def installSDL(path, deps):
    if len(deps) > 0 and not "sdl" in deps.keys():
        return

    print("Installing SDL...")

    version = []
    if len(deps) > 0:
        version = ["-v", f"{deps['sdl']}"]

    cwd = os.getcwd()
    os.chdir("sdl")

    buildPath = os.path.join(os.getcwd(), "build.py")
    installPath = os.path.join(os.getcwd(), "install.py")

    # build standard
    cmd = [f"{pythonPath}", f"{buildPath}"] + version
    runCmd(cmd)

    # build ios
    if platform.system() == "Darwin":
        cmd = [f"{pythonPath}", f"{buildPath}", "-ios"] + version
        runCmd(cmd)

    # install standard
    cmd = [f"{pythonPath}", f"{installPath}", "-p", f"{path}"] + version
    runCmd(cmd)

    # install ios
    if platform.system() == "Darwin":
        cmd = [f"{pythonPath}", f"{installPath}", "-p", f"{path}", "-ios"] + version
        runCmd(cmd)

        cmd = [f"{pythonPath}", f"{installPath}", "-p", f"{path}", "-iossim"] + version
        runCmd(cmd)

    os.chdir(cwd)

    print("Installed SDL.")


def installSDLimage(path, deps):
    if len(deps) > 0 and not "sdl_image" in deps.keys():
        return

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


def installSDLnet(path, deps):
    if len(deps) > 0 and not "sdl_net" in deps.keys():
        return

    print("Installing SDL net...")

    cwd = os.getcwd()
    os.chdir("sdl_net")

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

    print("Installed SDL net.")


def installSDLttf(path, deps):
    if len(deps) > 0 and not "sdl_ttf" in deps.keys():
        return

    print("Installing SDL ttf...")

    cwd = os.getcwd()
    os.chdir("sdl_ttf")

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

    print("Installed SDL ttf.")


def installSDLmixer(path, deps):
    if len(deps) > 0 and not "sdl_mixer" in deps.keys():
        return

    print("Installing SDL mixer...")

    cwd = os.getcwd()
    os.chdir("sdl_mixer")

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

    print("Installed SDL mixer.")


def installCatch2(path, deps):
    if len(deps) > 0 and not "catch2" in deps.keys():
        return

    print("Installing catch2...")

    cwd = os.getcwd()
    os.chdir("catch2")

    buildPath = os.path.join(os.getcwd(), "build.py")
    installPath = os.path.join(os.getcwd(), "install.py")

    # build standard
    cmd = [f"{pythonPath}", f"{buildPath}"]
    runCmd(cmd)

    # install
    cmd = [f"{pythonPath}", f"{installPath}", "-p", f"{path}"]
    runCmd(cmd)

    os.chdir(cwd)

    print("Installed catch2.")


def installNlohmannJson(path, deps):
    if len(deps) > 0 and not "nlohmann_json" in deps.keys():
        return

    print("Installing nlohmann json...")

    cwd = os.getcwd()
    os.chdir("nlohmann_json")

    installPath = os.path.join(os.getcwd(), "install.py")

    # install
    cmd = [f"{pythonPath}", f"{installPath}", "-p", f"{path}"]
    runCmd(cmd)

    os.chdir(cwd)

    print("Installed nlohmann json.")


def installlibSodium(path, deps):
    if len(deps) > 0 and not "libsodium" in deps.keys():
        return

    print("Installing libSodium...")

    cwd = os.getcwd()
    os.chdir("libsodium")

    buildPath = os.path.join(os.getcwd(), "build.py")
    installPath = os.path.join(os.getcwd(), "install.py")

    # build standard
    cmd = [f"{pythonPath}", f"{buildPath}"]
    runCmd(cmd)

    # install
    cmd = [f"{pythonPath}", f"{installPath}", "-p", f"{path}"]
    runCmd(cmd)

    # install ios
    # libSodium does not have a separate ios simulator build
    if platform.system() == "Darwin":
        cmd = [f"{pythonPath}", f"{buildPath}", "-ios"]
        runCmd(cmd)

        cmd = [f"{pythonPath}", f"{installPath}", "-p", f"{path}", "-ios"]
        runCmd(cmd)

    os.chdir(cwd)

    print("Installed libSodium.")


def installsqlite3(path, deps):
    if len(deps) > 0 and not "sqlite3" in deps.keys():
        return

    print("Installing sqlite3...")

    cwd = os.getcwd()
    os.chdir("sqlite3")

    buildPath = os.path.join(os.getcwd(), "build.py")
    installPath = os.path.join(os.getcwd(), "install.py")

    # build standard
    cmd = [f"{pythonPath}", f"{buildPath}"]
    runCmd(cmd)

    # install
    cmd = [f"{pythonPath}", f"{installPath}", "-p", f"{path}"]
    runCmd(cmd)

    os.chdir(cwd)

    print("Installed sqlite3.")


def installGLEW(path, deps):
    if len(deps) > 0 and not "glew" in deps.keys():
        return

    print("Installing GLEW...")

    cwd = os.getcwd()
    os.chdir("glew")

    buildPath = os.path.join(os.getcwd(), "build.py")
    installPath = os.path.join(os.getcwd(), "install.py")

    # build standard
    cmd = [f"{pythonPath}", f"{buildPath}"]
    runCmd(cmd)

    # install
    cmd = [f"{pythonPath}", f"{installPath}", "-p", f"{path}"]
    runCmd(cmd)

    os.chdir(cwd)

    print("Installed GLEW.")


def installNinja(path, deps):
    if len(deps) > 0 and not "ninja" in deps.keys():
        return

    print("Installing Ninja...")

    cwd = os.getcwd()
    os.chdir("ninja")

    buildPath = os.path.join(os.getcwd(), "build.py")
    installPath = os.path.join(os.getcwd(), "install.py")

    # build standard
    cmd = [f"{pythonPath}", f"{buildPath}"]
    runCmd(cmd)

    # install
    cmd = [f"{pythonPath}", f"{installPath}", "-p", f"{path}"]
    runCmd(cmd)

    os.chdir(cwd)

    print("Installed Ninja.")


print("Installing all dependencies...")

args = configureArguments()

deps = getProjectDependencies(args.path)

installPath = os.path.join(args.path, "libraries")

installClang(installPath, deps)

installv8(installPath, deps)

installSDL(installPath, deps)

installSDLimage(installPath, deps)

installSDLnet(installPath, deps)

installSDLttf(installPath, deps)

installSDLmixer(installPath, deps)

installCatch2(installPath, deps)

installNlohmannJson(installPath, deps)

installlibSodium(installPath, deps)

installsqlite3(installPath, deps)

installGLEW(installPath, deps)

installNinja(installPath, deps)

print("Installed all dependencies.")