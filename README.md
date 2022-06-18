# Javalang

⚠️ IF YOU USE THIS FOR PRODUCTION, IT IS AT YOUR OWN RISK ⚠️

A python script which "generates" a python wheel configuratoin for a specified OS and architecture of [Adoptium's](https://adoptium.net) JDK.

## Why?

I was inspired by the [ziglang](https://pypi.org/project/ziglang/) python package, so I decided to take [Adoptium's](https://adoptium.net) JDK and ship it as a python wheel.

## How do I use this?

After cloning the git repo, it's pretty simple, [gen-build-dir.py](gen-build-dir.py) does most of the heavy lifting:

```
$ python3 gen-build-dir.py -o linux -a x64
$ cd linux-x64-javalang
$ python -m build # you can make a venv first and install build within there if you want
```

Now you can find your wheel in `linux-x64-javalang/dist`. Once you install the wheel, you can use it just like [ziglang](https://pypi.org/project/ziglang/):

```python
import sys, subprocess

subprocess.call([sys.executable, "-m", "javalang"])
```

The operating system supported are:

 - linux
 - mac
 - windows

The architecture's are any architecture Adoptium supports for the particular OS.

## Usage

```
usage: gen-build-dir.py [-h] [-o os] [-a architecture] [-j java_ver]

Toggle switch ports for link testing.

options:
  -h, --help            show this help message and exit
  -o os, --operating-system os
                        Specify an operating system
  -a architecture, --architecture architecture
                        Specify an architecture
  -j java_ver, --java-version java_ver
                        Specify a version of java
```