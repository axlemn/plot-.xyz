Description
===========
Monitors a directory for changes to or new .xyz files and then runs feff6 on them, once for each Tantalum atom present.  Does not trigger when a file is moved into the directory.  

monitor\_changes.py runs an instance of watchdog, 
run\_script.py manages the data pipeline.  
xyz\_to\_feff.py manages data conversion.

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
----
- Modify setup.py file to include testfiles and check package installation
- Add feff processing and averaging
- Make output more sensible

Known bugs
----
- Processing when an old file is updated in Vim

Changelog 
----
- Deleted any use of a timestamp file, replacing it with an instance of watchdog.  
- Changed output files
- Modified checks to the .xyz file
