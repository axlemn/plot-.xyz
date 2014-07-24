Description
===========
Monitors a directory for changes to or new .xyz files and then runs feff6 on them, once for each Tantalum atom present.  Does not trigger when a file is moved into the directory.  

Installation
===========
Download the .tar.gz file under dist via the "View Raw" option.
Unpack the file:
tar -zxvf xyztofeff-0.1dev.tar.gz

Change directory to 
/xyztofeff-0.1dev/process\_xyz

To use, run: python monitor\_changes.py [path/to/watch]
The default directory is the one which contains the scripts.  

The xyz\_to\_feff program requires a couple of python packages, both of which can be installed via pip. 
pip install periodic
pip install watchdog

pip itself may be installed on Unix systems via:
pip install -U pip


TODO
====
- Modify setup.py file 
- Add feff processing and averaging
- Make output more sensible
- Include testfiles

Known bugs
=====
- Processing when an old file is updated in Vim

Changelog 
==========
- Deleted any use of a timestamp file, replacing it with an instance of watchdog.  
- Changed output files
- Modified checks to the .xyz file
