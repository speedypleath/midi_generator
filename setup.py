from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension

ext_modules = [
    Pybind11Extension("note",
                      ["lib/midi_generator/pybind.cpp"],
                      extra_compile_args=['-std=c++11']
                      ),
]

setup(ext_modules=ext_modules)
