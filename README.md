Description
===========
monitors a directory for changes to or new .xyz files and then runs various processing tools on them.  A timestamps file (default: timestamps.txt) is created once at the beginning of each session.  

Installation
===========
Download and unpack the .tar.gz file:
tar -zxvf \_\_.tar.gz

The xyz\_to\_feff program requires a couple of python packages, both of which can be installed via pip. 

pip install periodic
pip install watchdog

pip itself may be installed on Unix systems via:
pip install -U pip


Usage Notes
===========
To use, run "python monitor\_changes.py".

TODO
====
- Modify setup.py file 
- Add feff processing

Known bugs
=====
- Repetition of processing when an old file is updated

Changelog 
==========
- Deleted any use of a timestamp file, replacing it with an instance of watchdog.  

- Changed output files
- Modified checks to the .xyz file
