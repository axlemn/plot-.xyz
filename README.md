Description
===========
When a .xyz file is changed in a monitored directory, feff, ifeffit, and matplotlib are used to plot the chi(k) formed by averaging over all possible choices for a central atom of a specific element (by default, Tantalum).  

Made to work in \*nix.

Summary of each file (in order of usage):
==================
- watch\_for\_xyz takes in a directory to watch (by default the current directory), and contains the loop which tracks which files to update.  
- update\_xyz takes in a single file to update.

Files used to process\_xyz:
---------------
- run\_script.py manages most spawning of subprocesses.  update\_file is the main function, and determines what will happen to a files given by watch\_for\_xyz.
- helper.py holds several basic helper functions/constants
- xyz\_to\_feff.py takes in the path to an xyz file and some n, and prints a feff.inp file with the nth Ta atom at the center (n is zero-indexed).  Atoms are filtered here (currently: removed if outside of threshold distance).
- ifeffit\_script.ps takes a directory name, and uses all feff####.dat produced by feff in the directory to write a file containing chi(k) data.  
- matplotlib\_script.py averages chi(k) files, and controls what matplotlib will eventually plot.
- chir.ps converts chi.k files to chi.r files.  Called by the matplotlib\_script.

Usage
=====

After installation, run either 

    $ update_xyz FILENAME

or 

    $ watch_for_xyz [/dir/to/watch]

By default this watches your working directory.  

How to Obtain
===========
Download the .tar.gz file under dist via the "View Raw" option from GitHub.

Unpack the file:

    $tar -zxvf xyztofeff-0.1dev.tar.gz

Navigate to the new directory:

    $cd xyztofeff-0.1dev

Install via:

    $python setup.py install 

Most users will want to use sudo for the install step.
The "--record files.txt" is not necessary, but will make uninstallation slightly simpler.  

How to Uninstall
-------------
Navigate to the xyztofeff-0.1dev directory and run:

    $python setup.py install --record files.txt

Again, sudo may be necessary. 

Note that the commands may still appear to exist, since pip may not remove files in your /usr/local/bin directory.  This is fine if you intend to reinstall the program.  Otherwise, navigate to your /usr/local/bin and delete any files listed in files.txt.

Requirements
------------
The xyz\_to\_feff program requires a couple of python packages, both of which can be installed via pip. 

    $pip install periodic

    $pip install matplotlib

Instructions to install pip itself may be found [here](http://pip.readthedocs.org/en/latest/installing.html).

ifeffit and perl are also assumed to be installed, both of which can be installed through your package manager.  

Perhaps most tricky to install is the perl wrapper for ifeffit.  This can also be installed through the package manager, and (for OSX) should be automatically installed if you install Athena.  

TODO:
----
- Modify setup.py file to check for a functioning ifeffit perl wrapper
- Clean output to terminal per feff / ifeffit run
- Create logfile per run
- http://cars9.uchicago.edu/autobk/refman/node80.html

Known issues
----
- The message "Fatal Error: No absorbing atom (ipot=0) defined" probably means that the attempt at xyz conversion failed.  At this point, try running the test\_xyz\_converter.py script.

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
