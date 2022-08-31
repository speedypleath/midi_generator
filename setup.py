from setuptools import setup
from setuptools.extension import Extension
import sys

if sys.platform == 'darwin':
    from distutils import sysconfig
    vars = sysconfig.get_config_vars()
    vars['LDSHARED'] = vars['LDSHARED'].replace('-bundle', '-dynamiclib')

extensions = Extension('note',
                       sources=['src/lib/midi_generator/build.cpp'],
                       include_dirs=['/opt/homebrew/include'],
                       library_dirs=['/opt/homebrew/lib/lib'],
                       runtime_library_dirs=['/opt/homebrew/lib'],
                       libraries=['boost_python310'])

setup(ext_modules=[extensions])
