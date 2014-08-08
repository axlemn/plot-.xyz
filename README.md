Description
===========
When a .xyz file is changed in a monitored directory, feff, ifeffit, and matplotlib are used to plot the chi(k) formed by averaging over all possible choices for a central atom of a specific element (by default, Tantalum).  

Made to work in \*nix.

Summary of each file:
------------------
- timestamps.py initializes and watches a file storing a list of file names and their last modified times. 
- run\_script.py manages the data piping.  
- xyz\_to\_feff.py manages data conversion.  
- ifeffit\_script.ps runs ifeffit.  If you want to see what commands are run on which .dat files, look at the end of this file.  

To ignore automatic detection and manually run the data processing on a specific file, navigate to the process\_xyz folder and run:
python -c "from run\_script import update\_file; update\_file(FILENAME)"

Obtaining and Using
===========
Download the .tar.gz file under dist via the "View Raw" option from GitHub.

Unpack the file:
tar -zxvf xyztofeff-0.1dev.tar.gz

To start monitoring a directory, cd to 
/xyztofeff-0.1dev/process\_xyz

and run: python timestamps.py [path/to/watch]

To test, copy a valid .xyz file into the watched directory (sample .xyz files can be found in the testfiles folder).

The xyz\_to\_feff program requires a couple of python packages, both of which can be installed via pip. 
pip install periodic
pip install matplotlib

pip itself may be installed on Unix systems via:
pip install -U pip

ifeffit and perl are also assumed to be installed, both of which can be installed through your package manager.  

TODO:
----
- Modify setup.py file to check package installation, and add easy access to program via /usr/bin/
- Clean output to terminal per feff / ifeffit run
- Create logfile per run

Known issues
----
- None at the moment!

Changelog 
----
- Reverted to using a timestamp file
- Fixed issue with selecting other directories to monitor
- Replaced pgplot graphing with matplotlib
- Added perl ifeffit script and functionality
- Added creation of subdirectories and runs processing for each Ta atom
- Deleted any use of a timestamp file, replacing it with an instance of watchdog
- Changed output files
- Modified checks to the .xyz file
