import os
import shutil
import subprocess
import argparse
import platform
import zipfile

cwd = os.getcwd()

v8_version = "9.0"

v8_windows_binary_url = "https://github.com/snowmeltarcade/project-dependencies/releases/download/v8_9.0_Windows/v8_9.0.zip"
v8_darwin_binary_url = "https://github.com/richardjhughes/project-dependencies/releases/download/v8_9.0/v8_9.0_Darwin.zip"
v8_darwin_ios_binary_url = ""
v8_darwin_ios_simulator_binary_url = ""
v8_linux_binary_url = ""

v8_source_dir = os.path.join(cwd, "v8")
depot_tools_dir = os.path.join(v8_source_dir, "depot_tools")

out_dir = os.path.join(cwd, "out")
build_dir = os.path.join(out_dir, f"v8_{v8_version}")

build_env = os.environ
build_env["PATH"] = depot_tools_dir + ":" + build_env["PATH"]

build_env["DEPOT_TOOLS_WIN_TOOLCHAIN"] = "0"

git_path = shutil.which("git")
curl_path = shutil.which("curl")

def run_cmd(cmd):
    print(f"Running command: {cmd}")
    subprocess.run(cmd)


def run_cmd_env(cmd, env):
    print(f"Running command: {cmd}")
    subprocess.run(cmd, env=env)


def run_cmd_ignore_error(cmd):
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


def make_dir(dir):
    try:
        os.makedirs(dir, 0o755)
    except OSError:
        print(f"Failed to create dir: {dir}")
    else:
        print(f"Created dir: {dir}")


def remove_dir(dir):
    try:
        shutil.rmtree(dir)
    except OSError:
        print(f"Failed to remove dir: {dir}")
    else:
        print(f"Removed dir: {dir}")


def download_source():
    print("Downloading source...")

    make_dir(v8_source_dir)

    os.chdir(v8_source_dir)

    run_cmd([git_path, "clone", "https://chromium.googlesource.com/chromium/tools/depot_tools.git"])

    depot_tools_gclient = os.path.join(depot_tools_dir, "gclient.bat" if platform.system() == "Windows" else "gclient")
    depot_tools_fetch = os.path.join(depot_tools_dir, "fetch.bat" if platform.system() == "Windows" else "fetch")

    run_cmd_env([depot_tools_gclient], build_env)
    run_cmd_env([depot_tools_fetch, "v8"], build_env)

    os.chdir(os.path.join(v8_source_dir, "v8"))

    run_cmd([git_path, "fetch"])
    run_cmd([git_path, "checkout", "-b", f"branch-heads/{v8_version}"])

    run_cmd_env([depot_tools_gclient, "sync"], build_env)

    print("Source downloaded.")


def setup_build(build_for_ios, build_for_ios_simulator):
    print("Setting up build...")

    is_clang = "false" if platform.system() == "Windows" else "true"

    gn_settings_general = f"--args=is_component_build = false is_debug = false target_cpu = \"x64\" use_custom_libcxx = false v8_monolithic = true v8_use_external_startup_data = false is_clang = {is_clang}"
    gn_settings_ios = f"--args=enable_ios_bitcode = true ios_deployment_target = 10 is_component_build = false is_debug = false target_cpu = \"arm64\" target_os = \"ios\" use_custom_libcxx = false use_xcode_clang = true v8_enable_i18n_support = false v8_monolithic = true v8_use_external_startup_data = false v8_enable_pointer_compression = false"
    gn_settings_ios_simulator = f"--args=enable_ios_bitcode = true ios_deployment_target = 10 is_component_build = false is_debug = false target_cpu = \"x64\" target_os = \"ios\" use_custom_libcxx = false use_xcode_clang = true v8_enable_i18n_support = false v8_monolithic = true v8_use_external_startup_data = false v8_enable_pointer_compression = false"

    is_darwin = platform.system() == "Darwin"
    is_valid_ios_build_system = build_for_ios and is_darwin
    is_valid_ios_simulator_build_system = build_for_ios_simulator and is_darwin

    if (build_for_ios or build_for_ios_simulator) and not is_darwin:
        print("Cannot build ios when not building from MacOS.")
        return

    gn_settings = gn_settings_general

    if is_valid_ios_build_system:
        gn_settings = gn_settings_ios
    elif is_valid_ios_simulator_build_system:
        gn_settings = gn_settings_ios_simulator

    depot_tools_gn = os.path.join(depot_tools_dir, "gn.bat" if platform.system() == "Windows" else "gn")

    run_cmd_env([depot_tools_gn, "gen", build_dir, gn_settings],
                build_env)

    print("Build setup.")


def do_build():
    print("Performing build...")

    os.chdir(build_dir)

    depot_tools_ninja = os.path.join(depot_tools_dir, "ninja.exe" if platform.system() == "Windows" else "ninja")
    run_cmd_env([depot_tools_ninja, "-v"], build_env)

    print("Built.")


def save_results(build_for_ios, build_for_ios_simulator):
    print("Saving results...")

    include_source = os.path.join(v8_source_dir, "v8", "include")
    include_dest = os.path.join(cwd, "include")

    if os.path.isdir(include_dest):
        remove_dir(include_dest)

    shutil.copytree(include_source, include_dest)

    list_source = os.path.join(build_dir, "obj")
    print(list_source)

    libs = os.listdir(list_source)

    binary_out = get_binary_out_path(build_for_ios, build_for_ios_simulator)
    make_dir(binary_out)

    zip_path = get_output_zip_path(binary_out)

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_LZMA, allowZip64=True) as zip:
        for lib in libs:
            if lib.endswith(".a") or lib.endswith(".lib"):
                print(lib)
                # use zip as this will work natively on all platforms, including Windows
                zip.write(os.path.join(list_source, lib), lib)

    print("Results saved.")


def get_binary_out_path(build_for_ios, build_for_ios_simulator):
    platform_name = platform.system()

    if build_for_ios:
        platform_name = "iOS"
    elif build_for_ios_simulator:
        platform_name = "iOS_Simulator"

    binary_out = os.path.join(cwd, "lib", platform_name)

    return binary_out


def get_output_zip_path(binary_out_path):
    zip_path = os.path.join(binary_out_path, f"v8_{v8_version}.zip")

    return zip_path


def cleanup():
    print("Cleaning up previous build files & folders...")

    if os.path.isdir(out_dir):
        remove_dir(out_dir)

    if os.path.isdir(v8_source_dir):
        remove_dir(v8_source_dir)

    print("Cleaned up.")


def does_need_building(build_for_ios, build_for_ios_simulator):
    output_path = get_binary_out_path(build_for_ios, build_for_ios_simulator)
    zip_path = get_output_zip_path(output_path)

    needs_building = os.path.exists(zip_path)

    return not needs_building


def try_and_download_binaries(build_for_ios, build_for_ios_simulator):
    print("Trying to download pre-built binaries...")

    url = ""

    system_name = platform.system()
    if system_name == "Windows":
        url = v8_windows_binary_url
    elif system_name == "Darwin":
        if build_for_ios:
            url = v8_darwin_ios_binary_url
        elif build_for_ios_simulator:
            url = v8_darwin_ios_simulator_binary_url
        else:
            url = v8_darwin_binary_url
    elif system_name == "Linux":
        url = v8_linux_binary_url
    else:
        print(f"Unknown system name: {system_name}")
        return False

    if url == "":
        return False

    output_path = get_binary_out_path(build_for_ios, build_for_ios_simulator)
    zip_path = get_output_zip_path(output_path)

    result = download_binary(url, zip_path)

    print("Finished trying.")

    return result


def download_binary(url, output_path):
    print(f"Trying to download url: '{url}' to path: '{output_path}'")

    cmd = [curl_path, "--create-dirs", "-Lo", f"{output_path}", f"{url}"]

    if run_cmd_ignore_error(cmd):
        print(f"Downloaded binary: {url}")
        return True
    else:
        print(f"Failed to download binary: {url}")
        return False


print(f"Start building v8 version {v8_version}...")

parser = argparse.ArgumentParser(description="Build v8")
parser.add_argument("-c", "--clean", action="store_true", default=False, help="Clean previous build files & folders")
parser.add_argument("-ios", "--ios", action="store_true", default=False, help="Build for iOS. Note: Only valid for use when building on MacOS")
parser.add_argument("-iossim", "--ios-simulator", action="store_true", default=False, help="Build for iOS. Note: Only valid for use when building on MacOS")

args = parser.parse_args()

if does_need_building(args.ios, args.ios_simulator):
    if args.clean:
        cleanup()

    if try_and_download_binaries(args.ios, args.ios_simulator):
        print("Downloaded binaries. Skipping build.")
    else:
        print("Failed to downlaod binaries. Building...")

        download_source()

        setup_build(args.ios, args.ios_simulator)

        do_build()

        save_results(args.ios, args.ios_simulator)
else:
    print("v8 already built.")

print("v8 built.")
