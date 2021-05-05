import os
import shutil
import platform
import argparse
import subprocess

sdlVersion = "2.0.14"
sdlGitURL = "https://github.com/libsdl-org/SDL.git"

gitPath = shutil.which("git")
cmakePath = shutil.which("cmake")

def configureArguments():
    parser = argparse.ArgumentParser()
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


def build():
    print("Starting build...")

    cwd = os.getcwd()
    tempDirPath = os.path.join(cwd, "__temp")

    createDirectories(tempDirPath)

    os.chdir(tempDirPath)

    cmd = [gitPath, "clone", f"{sdlGitURL}"]
    runCmd(cmd)

    os.chdir(os.path.join(tempDirPath, "SDL"))

    cmd = [gitPath, "checkout", f"tags/release-{sdlVersion}", "-b", f"release-{sdlVersion}"]
    runCmd(cmd)

    os.chdir(cwd)

    #removeDirectory(tempDirPath)

    print("Finished build.")


print(f"Building SDL version {sdlVersion}...")

args = configureArguments()

build()

print(f"Built SDL version {sdlVersion}.")