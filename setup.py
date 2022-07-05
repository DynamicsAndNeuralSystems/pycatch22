from setuptools import setup, Extension, find_packages
import os

sourceDir = "C/";

sourceFileList = [sourceDir+file for file in os.listdir(sourceDir) if file.endswith(".c") and not 'main' in file]; #  and not (file == "sampen.c" or file == "run_features.c")];

# the c++ extension module
extension_mod = Extension(name="catch22_C",
	sources = [os.path.join("src","catch22","catch22_wrap.c")] + sourceFileList,
	include_dirs=["C"]) # Header files are here

# setup(name = "catch22", ext_modules=[extension_mod])

setup(
ext_modules = [extension_mod],
packages = find_packages(exclude=["test"]),
)
