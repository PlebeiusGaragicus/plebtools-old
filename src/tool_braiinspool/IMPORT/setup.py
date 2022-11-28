import io
import re
from glob import glob

from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import setup, find_packages

VERSION = '0.0.1'

setup(
    name='myAPI',
    #packages=['src/myAPI'],
    packages=find_packages('src/'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    version=VERSION,
    description='Does anybody really know what they are doing?',
    long_description=(open('README.md').read()),
    license="MIT",
    author='suchdatums',
    # author_email='mail@dbader.org',
    # url='https://github.com/dbader/envconfig',
    # download_url='https://github.com/dbader/envconfig/tarball/' + VERSION,
)
