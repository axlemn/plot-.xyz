Description
===========
monitors a directory for changes to or new .xyz files and then runs various processing tools on them.  A timestamps file (default: timestamps.txt) is created once at the beginning of each session.  

Requirements
===========
### python packages:
- periodic

Installation
===========
git clone git://github.com/axlemn/plot-and-transform-.xyz.git
pip install periodic

If pip is not installed, on unix systems run: 
pip install -U pip

Usage Notes
===========
main.sh dir [ts\_file]

The timestamp file to be used will be overwritten at the beginning of the session, currently without check.  
init\_timestamps and timestamp information acts as pseudo-replacement for inotify on osx systems.  

TODO
=========
watch and timestamp information will be replaced by watchdog (python package)
auto-install periodic via pip using the setup.py file (as well as checking for Athena or later software)

Changelog 
==========
- Changed output files
- Modified checks to the .xyz file
