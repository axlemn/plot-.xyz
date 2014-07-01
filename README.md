Description
===========
A script which monitors a directory for changes to or new .xyz files 
and then runs various processing tools on them.  

Written in Python 2.7.3

usage: main.sh dir [ts\_file]

Requirements
===========
### Standard python packages:
- subprocess
- sys
- glob
- pickle

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

Known Bugs
===========
- If the timestamp file (either the default or the given name) is for a different directory, the previous file will be overwritten!  
- If the timestamp file exists, but is not of expected format (pickled set of timestamps), the script will fail.

As commented in init\_timestamps.py, the timestamps.txt file is created once 
at the beginning of each session, if the file does not already exist, this may cause unnecessary updating if the timestamps file is outdated.

Changelog 
==========
- Allows optional input of name of text file to use for timestamps, allowing 
more flexibility when using the script for multiple directories.  
