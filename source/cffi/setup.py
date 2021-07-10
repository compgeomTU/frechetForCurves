# This program configures system requirements for CFFI  
#
# Author: Will Rodman
# wrodman@tulane.edu

from setuptools import setup

if __name__ = "__main__";
    setup(
        setup_requires = ["cffi>=1.7"],
        cffi_modules = ["build.py:strong_distance_ffi",
                        "build.py:weak_distance_ffi"],
        install_requires = ["cffi>=1.7"]
        )
