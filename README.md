Description
===========
When a .xyz file is changed in a monitored directory, feff6 is run for each Tantalum atom in the file, shifted each to the center in turn, and then all output files of format "feff####.dat" are grouped together in ifeffit.  Ifeffit plots each of these files in pgplot. 

Summary of each file:
------------------
monitor\_changes.py runs an instance of watchdog, 
run\_script.py manages the data pipeline.  
xyz\_to\_feff.py manages data conversion.
ifeffit\_sctip.py

Installation
===========
Download the .tar.gz file under dist via the "View Raw" option.

Unpack the file:
tar -zxvf xyztofeff-0.1dev.tar.gz

Change directory to 
/xyztofeff-0.1dev/process\_xyz

Usage
----
To use, run: python monitor\_changes.py [path/to/watch]
By default, the path watched is the process\_xyz directory.  

The xyz\_to\_feff program requires a couple of python packages, both of which can be installed via pip. 
pip install periodic
pip install watchdog

pip itself may be installed on Unix systems via:
pip install -U pip

ifeffit and perl are also assumed to be installed, both of which can be installed through your package manager.  

TODO
----
- Modify setup.py file to include testfiles and check package installation
- Add feff processing and averaging
- Clean output 

Known issues
----
- Processing multiple times when an old file is updated in Vim (this is a watchdog quirk, and appears unique to Vim)
- Only one pgplot window will stay open at a time

Changelog 
----
- Added perl ifeffit script and functionality
- Added creation of subdirectories and runs processing for each Ta atom

- Deleted any use of a timestamp file, replacing it with an instance of watchdog.  
- Changed output files
- Modified checks to the .xyz file
