# 07/07/14
# Alexander Mun

from setuptools import setup, find_packages

setup(
    name='xyztofeff',
    version='0.1dev',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['periodic', 'watchdog']
)
