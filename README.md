# project-dependencies
Common dependencies used by projects

## Usage

##### Correct as of: 2021-05-01

To install these dependencies, you need

* Python 3.6+

Building specific dependencies may require other dependencies. These are listed below as needed.

You can install everything by running `install_all.py`:

```
python3 install_all.py -p /path/to/project/
```

## Clang

##### Correct as of: 2021-05-30

By default, using version 12: https://github.com/llvm/llvm-project/releases/tag/llvmorg-12.0.0

To install, run `install.py`:

```
python3 install.py -p /path/to/install/directory/ -v version
```

`-v` is optional.

If using Linux, please note the Ubuntu 20.04 build of clang is downloaded.

## v8

##### Correct as of: 2021-05-30

By default, using version 9.0: https://v8.dev/blog/v8-release-90

To build, you need to install:

* Git
* Curl
* Build tools as specified here: https://v8.dev/docs/source-code#instructions

If building on Ubuntu, you need to set `python2` as the default python installation. See this StackOverflow post for more information: https://stackoverflow.com/q/60577790

To build, run `build.py`:

```
python3 build.py -v version
```

`-v` is optional.

This will build for the platform you are running this script on, be it Windows, Linux or Mac.

To build for iOS or the iOS simulator, you must run this script on MacOS.

For iOS, pass the `-ios` flag:

```
python3 build.py -ios
```

For the iOS simulator, pass the `-iossim` flag:

```
python3 build.py -iossim
```

This script tries its best to automate everything needed. In case you encounter an error, please see the official build and setup guides here:

https://v8.dev/docs/build

https://v8.dev/docs/source-code

Once built, you can install by running `install.py`:

```
python3 install.py -p /path/to/install/directory/ -v version
```

`-v` is optional.

This will install the v8 binaries based on the platform the script is running.

If you would like to install the iOS or iOS Simulator binaries, run `install.py` on MacOS with one of the following flags:

iOS:

```
python3 install.py -p /path/to/install/directory/ -ios
```

iOS Simulator:

```
python3 install.py -p /path/to/install/directory/ -iossim
```

## SDL

##### Correct as of 2021-05-30

By default, using version 2.0.14: https://github.com/libsdl-org/SDL/releases/tag/release-2.0.14

To build, you need to install:

* Git
* CMake
* Standard compiler setup for your platform (MSVC, Clang, GCC, Xcode etc...)

To build, run `build.py`:

```
python3 build.py -v version
```

`-v` is optional.

This will build for the platform you are running this script on, be it Windows, Linux or Mac.

To build for iOS, pass the `-ios` flag:

```
python3 build.py -ios
```

Note: this only works when building on MacOS.

To install, run `install.py`:

```
python3 install.py -p /path/to/install/directory -v version
```

`-v` is optional.

If running on MacOS, to install the iOS or iOS Simulator builds, pass the `-ios` or `-iossim` flags:

```
python3 install.py -p /path/to/install/directory -ios
python3 install.py -p /path/to/install/directory -iossim
```

## SDL Image

##### Correct as of 2021-05-30

By default, using version 2.0.5: https://github.com/libsdl-org/SDL_image/releases/tag/release-2.0.5

To build, you need to install:

* Git
* Standard compiler setup for your platform (MSVC, Clang, GCC, Xcode etc...)

To build on Linux, you also need to install:
* Autoconf
    ```
    sudo apt-get install autoconf
    ```

To build, run `build.py`:

```
python3 build.py -v version
```

`-v` is optional.

This will build for the platform you are running this script on, be it Linux or Mac.

Note: v2.0.5 is very difficult to build automatically on Windows. For now, please build manually using Visual Studio. You many need to add the `DLL_EXPORT` preprocessor definition.

To build for iOS, pass the `-ios` flag:

```
python3 build.py -ios
```

Note: this only works when building on MacOS. Please use Xcode to perform the actual builds for `iOS` and `iOS Simulator`. The `-ios` flag will try to download the prebuild releases only.

To install, run `install.py`:

```
python3 install.py -p /path/to/install/directory -v version
```

`-v` is optional.

If running on MacOS, to install the iOS or iOS Simulator builds, pass the `-ios` or `-iossim` flags:

```
python3 install.py -p /path/to/install/directory -ios
python3 install.py -p /path/to/install/directory -iossim
```

## SDL Net

##### Correct as of 2021-05-11

Using version 2.0.1: https://github.com/libsdl-org/SDL_net/releases/tag/release-2.0.1

To build, you need to install:

* Git
* Standard compiler setup for your platform (MSVC, Clang, GCC, Xcode etc...)

To build on Linux, you also need to install:
* Autoconf
    ```
    sudo apt-get install autoconf
    ```

To build, run `build.py`:

```
python3 build.py
```

This will build for the platform you are running this script on, be it Linux or Mac.

Note: v2.0.1 is very difficult to build automatically on Windows. For now, please build manually using Visual Studio. You many need to add the `DLL_EXPORT` preprocessor definition.

To build for iOS, pass the `-ios` flag:

```
python3 build.py -ios
```

Note: this only works when building on MacOS. Please use Xcode to perform the actual builds for `iOS` and `iOS Simulator`. The `-ios` flag will try to download the prebuild releases only.

To install, run `install.py`:

```
python3 install.py -p /path/to/install/directory
```

If running on MacOS, to install the iOS or iOS Simulator builds, pass the `-ios` or `-iossim` flags:

```
python3 install.py -p /path/to/install/directory -ios
python3 install.py -p /path/to/install/directory -iossim
```

## SDL TTF

##### Correct as of 2021-05-11

Using version 2.0.15: https://github.com/libsdl-org/SDL_ttf/releases/tag/release-2.0.15

To build, you need to install:

* Git
* Standard compiler setup for your platform (MSVC, Clang, GCC, Xcode etc...)

To build on Linux, you also need to install:
* Autoconf
    ```
    sudo apt-get install autoconf
    ```
* Freetype 6 Dev
    ```
    sudo apt-get install libfreetype6-dev
    ```

To build, run `build.py`:

```
python3 build.py
```

This will build for the platform you are running this script on, be it Linux or Mac.

Note: v2.0.15 is very difficult to build automatically on Windows. For now, please build manually using Visual Studio. You many need to add the `DLL_EXPORT` preprocessor definition.

To build for iOS, pass the `-ios` flag:

```
python3 build.py -ios
```

Note: this only works when building on MacOS. Please use Xcode to perform the actual builds for `iOS` and `iOS Simulator`. The `-ios` flag will try to download the prebuild releases only.

To install, run `install.py`:

```
python3 install.py -p /path/to/install/directory
```

If running on MacOS, to install the iOS or iOS Simulator builds, pass the `-ios` or `-iossim` flags:

```
python3 install.py -p /path/to/install/directory -ios
python3 install.py -p /path/to/install/directory -iossim
```

## SDL Mixer

##### Correct as of 2021-05-11

Using version 2.0.4: https://github.com/libsdl-org/SDL_mixer/releases/tag/release-2.0.4

To build, you need to install:

* Git
* Standard compiler setup for your platform (MSVC, Clang, GCC, Xcode etc...)

To build on Linux, you also need to install:
* Autoconf
    ```
    sudo apt-get install autoconf
    ```

To build, run `build.py`:

```
python3 build.py
```

This will build for the platform you are running this script on, be it Linux or Mac.

Note: v2.0.4 is very difficult to build automatically on Windows. For now, please build manually using Visual Studio. You many need to add the `DLL_EXPORT` preprocessor definition.

To build for iOS, pass the `-ios` flag:

```
python3 build.py -ios
```

Note: this only works when building on MacOS. Please use Xcode to perform the actual builds for `iOS` and `iOS Simulator`. The `-ios` flag will try to download the prebuild releases only.

To install, run `install.py`:

```
python3 install.py -p /path/to/install/directory
```

If running on MacOS, to install the iOS or iOS Simulator builds, pass the `-ios` or `-iossim` flags:

```
python3 install.py -p /path/to/install/directory -ios
python3 install.py -p /path/to/install/directory -iossim
```

## Catch2

##### Correct as of 2021-05-09

Using version 2.13.6: https://github.com/catchorg/Catch2/releases/tag/v2.13.6

This a source code only package, so no building required.

To install, run `install.py`:

```
python3 install.py -p /path/to/install/directory
```

## Nlohmann JSON

##### Correct as of 2021-05-09

Using version 3.9.1: https://github.com/nlohmann/json/releases/tag/v3.9.1

This a source code only package, so no building required.

To install, run `install.py`:

```
python3 install.py -p /path/to/install/directory
```

## libSodium

##### Correct as of 2021-05-14

Using version 1.0.18: https://github.com/jedisct1/libsodium/releases/tag/1.0.18

To build, you need to install:

* Git
* Standard compiler setup for your platform (MSVC, Clang, GCC, Xcode etc...)

To build on Linux, you also need to install:
* Autoconf
    ```
    sudo apt-get install autoconf
    ```
* libtool
    ```
    sudo apt-get install libtool
    ```

To build, run `build.py`:

```
python3 build.py
```

This will build for the platform you are running this script on, be it Linux or Mac.

Note: Please manually build on Windows using Visual Studio. See the MSVC packages in `builds -> msvc`.

To build for iOS, pass the `-ios` flag:

```
python3 build.py -ios
```

Note: This will build a universal iOS binary, which includes the iOS Simulator.

To install, run `install.py`:

```
python3 install.py -p /path/to/install/directory
```

If running on MacOS, to install the iOS build, pass the `-ios` flag:

```
python3 install.py -p /path/to/install/directory -ios
```

## sqlite3

##### Correct as of 2021-05-12

Using version 3.35.5: https://github.com/sqlite/sqlite/releases/tag/version-3.35.5

To build, you need to install:

* Git
* Standard compiler setup for your platform (MSVC, Clang, GCC, Xcode etc...)

To build, run `build.py`:

```
python3 build.py
```

This will build for the platform you are running this script on, be it Linux or Mac. Building on Windows is not supported.

To install, run `install.py`:

```
python3 install.py -p /path/to/install/directory
```

## glew

##### Correct as of 2021-05-17

Using version 2.2.0: https://github.com/nigels-com/glew/releases/tag/glew-2.2.0

To build, you need to install:

* CMake
* Standard compiler setup for your platform (MSVC, Clang, GCC, Xcode etc...)

To build, run `build.py`:

```
python3 build.py
```

This will build for the platform you are running this script on, be it Linux, Mac or Windows.

Note: There is no iOS build, as glew is not used on iOS.

To install, run `install.py`:

```
python3 install.py -p /path/to/install/directory
```

## License

![GitHub](https://img.shields.io/github/license/snowmeltarcade/project-dependencies?style=plastic)