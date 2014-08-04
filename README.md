Description
===========
When a .xyz file is changed in a monitored directory, feff6 is run for each Tantalum atom in the file, shifted each to the center in turn, and then all output files of format "feff####.dat" are grouped together in ifeffit.  Ifeffit plots each of these files in pgplot. 

Made to work in \*nix.

Summary of each file:
------------------
monitor\_changes.py runs an instance of watchdog. 
run\_script.py manages the data piping.  
xyz\_to\_feff.py manages data conversion.  
ifeffit\_script.ps runs ifeffit.  If you want to see what commands are run on which .dat files, look at the end of this file.  

To ignore the automatic detection and manually run the data processing on a file, navigate to the process\_xyz folder and run:
python -c "from run\_script import update\_file; update\_file(FILENAME)"

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

To test, copy a valid .xyz file into the watched directory (sample .xyz files can be found in the testfiles folder).

The xyz\_to\_feff program requires a couple of python packages, both of which can be installed via pip. 
pip install periodic
pip install watchdog

pip itself may be installed on Unix systems via:
pip install -U pip

ifeffit and perl are also assumed to be installed, both of which can be installed through your package manager.  

TODO:
- Modify setup.py file to check package installation
- Add feff averaging
- Clean output 

Known issues
----
- Processing multiple times when an old file is updated in Vim (this is a watchdog quirk, unique to Vim)
- Some files are not read from general locations, causing issues if a folder other than the default is monitored

Changelog 
----
- Replaced pgplot graphing with matplotlib
- Added perl ifeffit script and functionality
- Added creation of subdirectories and runs processing for each Ta atom

- Deleted any use of a timestamp file, replacing it with an instance of watchdog.  
- Changed output files
- Modified checks to the .xyz file
