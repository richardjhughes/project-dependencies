import os
import shutil
import platform
import argparse
import subprocess
import zipfile

version = "2.3.0"
gitURL = "https://github.com/GPUOpen-LibrariesAndSDKs/VulkanMemoryAllocator.git"

gitPath = shutil.which("git")

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
    installDir = os.path.join(path, "vulkan_memory_allocator")

    return installDir


def isAlreadyInstalled(path):
    installDir = getFullInstallDir(path)

    filesExist = os.path.exists(installDir)

    return filesExist


def install(path):
    cwd = os.getcwd()

    # get the source code
    tempDirPath = os.path.join(cwd, "__temp", "vulkan_memory_allocator")
    createDirectories(tempDirPath)

    os.chdir(tempDirPath)

    cmd = [gitPath, "clone", f"{gitURL}"]
    runCmd(cmd)

    vmaPath = os.path.join(os.getcwd(), "VulkanMemoryAllocator")
    os.chdir(vmaPath)

    # checkout the version we want
    cmd = [gitPath, "checkout", f"tags/v{version}", "-b", f"v{version}"]
    runCmd(cmd)

    installDir = getFullInstallDir(path)
    createDirectories(installDir)

    # the src path is different to master
    header_src_path = os.path.join(vmaPath, "src", "vk_mem_alloc.h")
    header_dest_path = os.path.join(installDir, "vk_mem_alloc.h")

    shutil.copyfile(header_src_path, header_dest_path)

    os.chdir(cwd)


print("Installing vulkan memory allocator...")

args = configureArguments()

if args.version is not None and len(args.version) > 0:
    version = args.version

if isAlreadyInstalled(args.path):
    print("vulkan memory allocator already installed.")
else:
    install(args.path)

print("Installed vulkan memory allocator.")
