# 07/07/14
# Alexander Mun

import periodic
import matplotlib.pyplot
from setuptools import setup, find_packages

setup(
    name='xyztofeff',
    version='0.1dev',
    packages=find_packages(),
    include_package_data=True,
    scripts=['watch_for_xyz', 'update_xyz'],
    install_requires=['periodic']
)
