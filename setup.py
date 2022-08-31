from setuptools import setup
from setuptools.extension import Extension

extensions = Extension('note',
                       sources=['src/lib/midi_generator/build.cpp'],
                       include_dirs=['/usr/include'],
                       library_dirs=['/usr/lib'],
                       runtime_library_dirs=['/usr/lib'],
                       libraries=[':libboost_python310.so'])

setup(ext_modules=[extensions])
