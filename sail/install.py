import os
import shutil
import subprocess

# SAIL has a spider web of dependencies of its own, building it automatically and reproducibly on different
# platforms is difficult - for now, just use the published binaries
brewPath = shutil.which("brew")

def runCmd(cmd, cwd=None):
    print(f"Running command: {cmd}")
    subprocess.run(cmd, cwd=cwd)


def install():
    cmd = [brewPath, "install", "happyseafox/sail/sail"]
    runCmd(cmd)


print("Installing SAIL...")

install()

print("Installed SAIL.")
