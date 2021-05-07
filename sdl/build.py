import os
import shutil
import platform
import argparse
import subprocess
import zipfile

sdlVersion = "2.0.14"
sdlGitURL = "https://github.com/libsdl-org/SDL.git"

sdlDownloadURLWindows = ""
sdlDownloadURLDarwin = "https://github.com/snowmeltarcade/project-dependencies/releases/download/SDL_2.0.14/2.0.14_Darwin.zip"
sdlDownloadURLiOS = ""
sdlDownloadURLLinux = ""

gitPath = shutil.which("git")
cmakePath = shutil.which("cmake")
curlPath = shutil.which("curl")

def configureArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-ios", "--build-ios", action="store_true", required=False, help="build iOS binaries")
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


def build(buildiOS, tempDirPath):
    print("Starting build...")

    if platform.system() != "Darwin" and buildiOS:
        print("Can only build iOS on MacOS.")
        return

    createDirectories(tempDirPath)

    os.chdir(tempDirPath)

    # get the latest SDL code
    cmd = [gitPath, "clone", f"{sdlGitURL}"]
    runCmd(cmd)

    os.chdir(os.path.join(os.getcwd(), "SDL"))

    # checkout the version we want
    cmd = [gitPath, "checkout", f"tags/release-{sdlVersion}", "-b", f"release-{sdlVersion}"]
    runCmd(cmd)

    if buildiOS:
        # as of version 2.0.14, the cmake ios build isn't working
        buildDir = os.path.join(os.getcwd(), "build-scripts")
        os.chdir(buildDir)

        cmd = ["./iosbuild.sh"]
        runCmd(cmd)
    else:
        # build with cmake
        buildDir = os.path.join(os.getcwd(), "build")
        createDirectories(buildDir)
        os.chdir(buildDir)

        cmd = [cmakePath, ".."]
        runCmd(cmd)

        cmd = [cmakePath, "--build", "."]
        runCmd(cmd)

    os.chdir(cwd)

    print("Finished build.")


def saveResults(buildiOS, tempDirPath):
    print("Saving results...")

    sdlPath = os.path.join(tempDirPath, "SDL")
    buildDir = os.path.join(sdlPath, "build")

    platformLibName = getPlatformLibName(buildiOS)

    destIncludeDir = os.path.join(os.getcwd(), "include")
    destLibDir = os.path.join(os.getcwd(), "lib", platformLibName)

    createDirectories(destIncludeDir)
    createDirectories(destLibDir)

    # save includes
    shutil.copytree(os.path.join(sdlPath, "include"), destIncludeDir, dirs_exist_ok=True)

    # save binaries
    zipDir = getZipPath(destLibDir, platformLibName)

    with zipfile.ZipFile(zipDir, "w") as zip:

        # SDL_config.h is platform specific, so save it in the zip file
        zip.write(os.path.join(buildDir, "include", "SDL_config.h"), "SDL_config.h")

        if platform.system() == "Windows":
            zip.write(os.path.join(buildDir, "libSDL2.lib"), "libSDL2.lib")
            zip.write(os.path.join(buildDir, "libSDL2main.lib"), "libSDL2main.lib")
        else:
            zip.write(os.path.join(buildDir, "libSDL2.a"), "libSDL2.a")
            zip.write(os.path.join(buildDir, "libSDL2main.a"), "libSDL2main.a")

    print("Saved results.")


def getPlatformLibName(buildiOS):

    if platform.system() == "Darwin" and buildiOS:
        return "iOS"

    return platform.system()


def getZipPath(destLibDir, platformLibName):
    return os.path.join(destLibDir, f"{sdlVersion}_{platformLibName}.zip")


def doesNeedBuilding(buildiOS):
    platformLibName = getPlatformLibName(buildiOS)

    destIncludeDir = os.path.join(os.getcwd(), "include")
    destLibDir = os.path.join(os.getcwd(), "lib", platformLibName)

    zipDir = getZipPath(destLibDir, platformLibName)

    isBuilt = (os.path.exists(destIncludeDir) and
               os.path.exists(zipDir))

    return not isBuilt


def tryAndDownloadBinaries(buildiOS):
    print("Trying to download pre-built binaries...")

    url = ""

    system_name = platform.system()
    if system_name == "Windows":
        url = sdlDownloadURLWindows
    elif system_name == "Darwin":
        if buildiOS:
            url = sdlDownloadURLiOS
        else:
            url = sdlDownloadURLDarwin
    elif system_name == "Linux":
        url = sdlDownloadURLLinux
    else:
        print(f"Unknown system name: {system_name}")
        return False

    if url == "":
        return False

    platformLibName = getPlatformLibName(buildiOS)

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


print(f"Building SDL version {sdlVersion}...")

args = configureArguments()

cwd = os.getcwd()
tempDirPath = os.path.join(cwd, "__temp")

if doesNeedBuilding(args.build_ios):
    if tryAndDownloadBinaries(args.build_ios):
        print("Downloaded pre-built binaries.")
    else:
        build(args.build_ios, tempDirPath)

        saveResults(args.build_ios, tempDirPath)
else:
    print("SDL is already built...")

print(f"Built SDL version {sdlVersion}.")