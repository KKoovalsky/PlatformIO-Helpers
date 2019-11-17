# PlatformIO Helpers

## mbedignore.py

This script allows to ignore specific directories within the mbed-os framework run under PlatformIO.

It runs on Python3.

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

3. [Enable use of pre-script in PlatformIO](https://docs.platformio.org/en/latest/projectconf/advanced_scripting.html)
 and put that section to the `extra_script.py`:

```
from os import path
import sys

import mbedignore

Import("env")

ROOT_DIR = env['PROJECT_DIR']

mbedignore_path = path.join(ROOT_DIR, '.mbedignore')
mbed_os_dir = '/home/username/.platformio/packages/framework-mbed'

# Does the job related to ignoring the paths. 
mbedignore.apply(mbedignore_path, mbed_os_dir)
```

Tune the paths according to your environment.
