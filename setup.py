from setuptools import setup, Extension, find_packages
import sysconfig
import os

# Upstream catch22 C sources live in a git submodule (src/catch22); the
# pycatch22-specific CPython wrapper lives alongside it in src/wrapper.
upstreamDir = os.path.join("src", "catch22", "C")
wrapDir = os.path.join("src", "wrapper")

sourceFileList = [os.path.join(upstreamDir, file) for file in os.listdir(upstreamDir) if file.endswith(
    ".c") and not 'main' in file]
sourceFileList.append(os.path.join(wrapDir, "catch22_wrap.c"))

cflags = sysconfig.get_config_var('CFLAGS')
if cflags is not None:
    extra_compile_args = cflags.split()
else: # Windows system
    extra_compile_args = []

extra_compile_args += ["-std=c99"]

# The c++ extension module:
extension_mod = Extension(name = "catch22_C",
    sources = sourceFileList,
    include_dirs = [upstreamDir],
    extra_compile_args = extra_compile_args)  # Header files are here

setup(
    packages = find_packages(where = "src",
                            include = ["pycatch22"]),
    package_dir = {"": "src"},
    ext_modules = [extension_mod]
)
