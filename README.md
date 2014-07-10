Description
===========
A script which monitors a directory for changes to or new .xyz files 
and then runs various processing tools on them.  

A timestamps file (default: timestamps.txt) is created once at the beginning of each session.  

Note: If the file is not stored between sessions or files were already updated, this may cause unneeded updating.  If the file is for a different directory, 
it will be overwritten.  

Written in Python 2.7.3

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

Usage: 
------
main.sh dir [ts\_file]


Usage Notes
===========
- If the timestamp file named (or default) is meant for a different directory, the previous file will be overwritten, currently without check.
- If the timestamp file exists, but is not of expected format (pickled set of timestamps), the script will fail.  This is usually harmless, but may result in overwriting of the timestamp file.

init_timestamps and timestamp information acts as pseudo-replacement for inotify on osx systems.  

TODO
=========
watch and timestamp information will be replaced by watchdog (python package)
auto-install periodic via pip using the setup.py file (as well as checking for Athena or later software)

Changelog 
==========
- Changed output files
- Modified checks to the .xyz file
