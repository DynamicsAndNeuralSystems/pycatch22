from setuptools import setup, Extension, find_packages
import sysconfig
import os

sourceDir = os.path.join("src", "C");

sourceFileList = [os.path.join(sourceDir, file) for file in os.listdir(sourceDir) if file.endswith(
    ".c") and not 'main' in file]
    # and not (file == "sampen.c" or file == "run_features.c")]

extra_compile_args = sysconfig.get_config_var('CFLAGS').split()
extra_compile_args += ["-std=c99"]

# The c++ extension module:
extension_mod = Extension(name = "catch22_C",
    sources = sourceFileList,
    include_dirs = [sourceDir],
    extra_compile_args = extra_compile_args)  # Header files are here

setup(
    packages = find_packages(where = "src",
                            include = ["pycatch22"]),
    package_dir = {"": "src"},
    ext_modules = [extension_mod]
)
