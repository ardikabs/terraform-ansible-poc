

from setuptools import setup, find_packages, find_namespace_packages
from blog import (
    __version__,
    __author__,
    __email__,
    __url__
)
setup(
    name='blog',
    version=__version__,
    author=__author__,
    author_email=__email__,
    url=__url__,
    install_requires=['click', 'fabric', 'click_configfile'],
    include_package_data=True,
    packages=find_packages(),
    entry_points='''
        [console_scripts]
        cerberus=blog.cli:cli
    ''',
)