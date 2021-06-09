# PlatformIO Helpers

**NOTE:** See [Copper-Bot's fork](https://github.com/Copper-Bot/PlatformIO-Helpers) since it is more up-to-date.

Python3 is only supported.

For those helpers to work you should 
[enable use of pre-script in PlatformIO](https://docs.platformio.org/en/latest/projectconf/advanced_scripting.html)
and put that section to the `extra_script.py`:

```
from os import path
import sys

Import("env")

root_dir = env['PROJECT_DIR']

sys.path.append(path.join(root_dir, 'scripts'))

```


## mbedignore.py

This script allows to ignore specific directories within the mbed-os framework run under PlatformIO.

You should be able to use this script freely across different projects without interfering each other,
when ignoring specific paths within the mbed-os framework. 

The script needs `.mbedignore` file as input and also the path to the mbed-os framework. See 
[How to use it](#how-to-use-it).

`.mbedignore` shall contain relative paths which are to be ignored within the mbed-os framework, e.g.:

```
features/cellular
drivers/source/usb
components/wifi
```

Before you use it, it is suggested to run:

```
git init
git add .
git commit -m "Baseline"
```

in the mbed-os framework directory, which is most probably `~/.platformio/packages/framework-mbed`.

You'll be protected against unintented changes made by the script.

### How to use it

1. Create your `.mbedignore` file and put it e.g. in the root directory of your PlatformIO-based project.

2. Copy `mbedignore.py` script to the e.g. the root directory of your project.

3. Put that section to the `extra_script.py`:

```
import mbedignore
mbedignore_path = path.join(ROOT_DIR, '.mbedignore')
mbed_os_dir = '/home/username/.platformio/packages/framework-mbed'

# Does the job related to ignoring the paths. 
mbedignore.apply(mbedignore_path, mbed_os_dir)
```

Tune the paths according to your environment.

## custom_library_json.py

This script allows to apply a custom `library.json` file to any external library. It is assumed that the external
library is downloaded using `lib_deps` inside `platformio.ini`.

*NOTE:* When using the program in the pre-script the `library.json` will be not copied on the first build. This is
because the `library.json` is applied before the PIO's `build` target which downloads all the dependencies on the first
run. On the second build invocation the `library.json` should be applied correctly.


### How to use it

1. Prepare your custom `library.json` file for a specific library.

2. Put the file into a subdirectory within the project directory tree. The path shall be constructed like that:

```
<root directory of the project>/<path1>/<library name>
```

`path1` will contain all the custom `library.json` files. Within this path each subdirectory will have a name of a
library you want to apply the custom `library.json`. Each of those subdirectories will contain respective
`library.json` file, e.g.:

```
lib_overlay
    |____boost
            |____library.json
    |____unity
            |____library.json
    |____googleTest
            |____library.json
```

In the example `path1` is `lib_overlay`.

3. Put that section to the `extra_script.py`:

```
import custom_library_json
custom_library_json.apply(env, 'path1', 'library name')
```

Tune the paths according to your environment.
