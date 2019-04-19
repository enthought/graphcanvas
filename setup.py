# (C) Copyright 2009-2019 Enthought, Inc., Austin, TX
# All rights reserved.

from os.path import join
from setuptools import setup, find_packages


info = {}
with open(join('graphcanvas', '__init__.py')) as f:
    exec(f.read(), info)


setup(
    name='graphcanvas',
    version=info['__version__'],
    author='Bryce Hendrix',
    author_email='info@enthought.com',
    maintainer='ETS Developers',
    maintainer_email='enthought-dev@enthought.com',
    url='https://github.com/enthought/graphcanvas',
    download_url=(
        'https://github.com/enthought/graphcanvas/archive/'
        '{}.tar.gz'.format(info['__version__'])
    ),
    classifiers=[c.strip() for c in """\
        Development Status :: 5 - Production/Stable
        Intended Audience :: Developers
        Intended Audience :: Science/Research
        License :: OSI Approved :: BSD License
        Operating System :: MacOS
        Operating System :: Microsoft :: Windows
        Operating System :: OS Independent
        Operating System :: POSIX
        Operating System :: Unix
        Programming Language :: C
        Programming Language :: Python
        Topic :: Scientific/Engineering
        Topic :: Software Development
        Topic :: Software Development :: Libraries
        """.splitlines() if len(c.strip()) > 0],
    description='interactive graph visualization',
    long_description=open('README.rst').read(),
    ext_modules=[],
    include_package_data=True,
    install_requires=info['__requires__'],
    license='BSD',
    packages=find_packages(),
    platforms=["Windows", "Linux", "Mac OS-X", "Unix", "Solaris"],
    zip_safe=False,
)
