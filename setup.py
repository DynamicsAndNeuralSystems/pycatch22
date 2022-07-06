from setuptools import setup, Extension, find_packages
import os

sourceDir = os.path.join("src", "C");

sourceFileList = [os.path.join(sourceDir, file) for file in os.listdir(sourceDir) if file.endswith(
    ".c") and not 'main' in file]
    # and not (file == "sampen.c" or file == "run_features.c")]

# The c++ extension module:
extension_mod = Extension(name = "catch22_C",
    sources = sourceFileList,
    include_dirs = [sourceDir])  # Header files are here

setup(
    packages = find_packages(where = "src",
                            include = ["pycatch22"]),
    package_dir = {"": "src"},
    ext_modules = [extension_mod]
)
