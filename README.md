Description
===========
A script which monitors a directory for changes to or new .xyz files 
and then runs various processing tools on them.  

A timestamps file (default: timestamps.txt) is created once at the beginning of each session.  

Note: If the file is not stored between sessions or files were already updated, this may cause unneeded updating.  If the file is for a different directory, 
it will be overwritten.  

Written in Python 2.7.3

usage: main.sh dir [ts\_file]

Requirements
===========
### Standard python packages:
- subprocess
- sys
- glob
- pickle

- periodic


### Script applies following programs: 
- Avogadro
- Athena
- IFEFFIT
- FEFF6

How to Modify
===========
The basic script periodically regexes the directory contents for a particular 
filetype, then applies a script to any files changed in the past 5 seconds.  

To change the regex applied, change init\_timestamps.regex.  To change what command is run, edit the update function in run\_script.py.  Update interval is controlled by the call to watch in main.sh.

Usage Notes
===========
Be cautious with timestamps file if you write several to the same place.  
- If the timestamp file named (or default) is meant for a different directory, the previous file will be overwritten, currently without check.
- If the timestamp file exists, but is not of expected format (pickled set of timestamps), the script will fail.  This is usually harmless, but may result in overwriting of the timestamp file.

Changelog 
==========
- Changed output files
- Modified checks to the .xyz file
