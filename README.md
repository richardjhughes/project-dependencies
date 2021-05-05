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

##### Correct as of: 2021-05-04

Using version 12: https://github.com/llvm/llvm-project/releases/tag/llvmorg-12.0.0

To install, run `install.py`:

```
python3 install.py -p /path/to/install/directory/
```

If using Linux, please note the Ubuntu 20.04 build of clang is downloaded.

## v8

##### Correct as of: 2021-05-02

Using version 9.0: https://v8.dev/blog/v8-release-90

To build, you need to install:

* Git
* Curl
* Build tools as specified here: https://v8.dev/docs/source-code#instructions

If building on Ubuntu, you need to set `python2` as the default python installation. See this StackOverflow post for more information: https://stackoverflow.com/q/60577790

To build, run `build.py`:

```
python3 build.py
```

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
python3 install.py -p /path/to/install/directory/
```

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

## License

![GitHub](https://img.shields.io/github/license/snowmeltarcade/project-dependencies?style=plastic)