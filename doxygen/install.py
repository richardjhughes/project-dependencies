import os
import shutil
import subprocess

# As this is a tool used for documentation, there is no need build it
brewPath = shutil.which("brew")

def runCmd(cmd, cwd=None):
    print(f"Running command: {cmd}")
    subprocess.run(cmd, cwd=cwd)


def install():
    cmd = [brewPath, "install", "doxygen"]
    runCmd(cmd)


print("Installing doxygen...")

install()

print("Installed doxygen.")
