from setuptools import setup, Extension, find_packages
import os

sourceDir = os.path.join("src","C");

sourceFileList = [os.path.join(sourceDir, file) for file in os.listdir(sourceDir) if file.endswith(
    ".c") and not 'main' in file]
    # and not (file == "sampen.c" or file == "run_features.c")]

# The c++ extension module:
extension_mod = Extension(name="catch22_C",
    sources = sourceFileList,
	include_dirs = [sourceDir]) # Header files are here

# [os.path.join("C", "catch22_wrap.c")],
# setup(name = "catch22", ext_modules=[extension_mod])

setup(
    name = "pycatch22",
    include_dirs = [sourceDir],
    ext_modules = [extension_mod],
    packages = find_packages(exclude=["test"])
)
