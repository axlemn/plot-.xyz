# 07/07/14
# Alexander Mun

from setuptools import setup

setup(
    name='xyztofeff',
    version='0.1dev',
    packages=['process_xyz',],

    # Trying to get python to install numpy here.  >.>  
    install_requires=['BeautifulSoup'],
    long_description=open('README.md').read(),
)
