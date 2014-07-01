Description
===========
A script which monitors a directory for changes to or new .xyz files 
and then runs various processing tools on them.  

Written in Python 2.7.3

Usage 
-----
main.sh dir

Requirements
===========

Uses following:  
-watch (Unix utility)

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

To change the regex applied, change init\_timestamps.regex.
To change what command is run, edit the update function in run\_script.py.  
Update interval is controlled by the option to watch in main.sh.

Known Bugs
===========
As commented in init\_timestamps.py, the timestamps.txt file is created once 
at the beginning of each session if the file does not already exist.  This causes a problem if :

- The timestamp file is for a different directory (existing file will be overwritten!).  
- The timestamp file is not of expected format (pickled set of timestamps).

