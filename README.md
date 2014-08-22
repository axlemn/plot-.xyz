Description
===========

plot.xyz is an EXAFS processing tool which takes in an .xyz file and displays its chi(k) and chi(r) data in matplotlib.  

There are two different commands.  The watch\_for\_xyz command will display the chi(r) and chi(k) data of any .xyz files modified or added to a specified directory while it is running.  This allows users to use a program such as Avagadro to edit xyz files and immediately see plots of chi(r) and chi(k) data.  This allows users to tune .xyz files based on immediately accessible EXAFS data.  

Made to work in Unix.  It should also work in Windows, but has only been tested in Linux. 

How it Works
=============
When a .xyz file is changed in a monitored directory, the watch\_for\_xyz script passes the filename is given to the function update\_file.  

An input file to feff requires designation of a center, absorbing atom, and at most 500 atoms, so the .xyz file is then converted into #ofTaAtoms feff.inp files, each in their own subdirectory.  Ifeffit provides more options for chi(k) plots than feff does, but since it does not calculate path files, feff is used to calculate paths instead the feff defaults are used.

Finally, the data from Ifeffit is processed and displayed via matplotlib.

As a Diagram
-------
<img src="https://github.com/axlemn/plot-.xyz/blob/master/flow_chart.png">
Image courtesy of [ditaa](ditaa.sourceforge.net/).  

Summary of each file (in order of usage):
==================
- watch\_for\_xyz takes in a directory to watch (by default the current directory), and contains the loop which tracks which files to update.  
- update\_xyz takes in a single file to update.
Both options only act on files by calls to run\_script.update\_file(FILENAME). 
- run\_script.py manages most spawning of subprocesses.  update\_file(FILENAME) is the main function. 
- helper.py holds simple, universal functions/constants
- temp.txt stores metadata, such as center of mass, which atoms are close to the center of mass, etc. 
- xyz\_to\_feff.py takes in the path to a .xyz file and some n, and prints a feff.inp file with the nth Ta atom as the absorbing atom.  n is zero-indexed.  
- ifeffit\_script.ps takes a directory name, and uses all feff####.dat produced by feff in the directory to write a file containing chi(k) data.  
- matplotlib\_script.py averages chi(k) files, and controls what matplotlib will eventually plot.
- chir.ps converts chi.k files to chi.r files.  Called by the matplotlib\_script.

Usage
=====

After installation, run either 

    $ update_xyz FILENAME [FLAGS]

or 

    $ watch_for_xyz [/dir/to/watch]

By default watch\_for\_xyz watches your working directory.  

    Flags for update_xyz:
    -m will skip the displaying graphs step.
    -e will use only paths from atoms nearby the center_of_mass 
    -n will avoid re-calculating paths in feff, i.e. assumes that the file 
        is already up-to-date and skips straight to calculating the average
        chi(k) and graphing.  

How to Obtain / Update
===========
Download the .tar.gz file under dist via the "View Raw" option from GitHub.

Unpack the file:

    $ tar -zxvf xyztofeff-0.1dev.tar.gz

Navigate to the new directory:

    $ cd xyztofeff-0.1dev

Install via:

    $ python setup.py install 

Most users will want to use sudo for the install step.

The same command can also be used to install any changes made to files in the xyztofeff directory.  

How to Uninstall
-------------
Navigate to the xyztofeff-0.1dev directory and run:

    $ python setup.py install --record files.txt

Again, sudo may be necessary.  This will write the locations all files which were created during installation to the folder "files.txt".  

To remove most of them, run 

    $ pip uninstall xyztofeff

with sudo if you installed the program with sudo.

Note that the commands may still appear to exist, since pip may not remove files in your /usr/local/bin directory.  This is fine if you intend to reinstall the program.  Otherwise, navigate to your /usr/local/bin and delete any files listed in files.txt.

Dependencies
------------
The xyz\_to\_feff program requires a couple of python packages, both of which can be installed via pip. 

    $ pip install periodic

    $ pip install matplotlib

Instructions to install pip itself may be found [here](http://pip.readthedocs.org/en/latest/installing.html).

ifeffit and perl are also assumed to be installed, both of which can be installed through your package manager for Linux.  

Perhaps the most tricky requirement to install is the perl wrapper for ifeffit.  This can also be installed through the package manager, and (for OSX) should be automatically installed if you install Athena.  To check if you have the perl wrapper installed, run: 

    $ perl -de "use Ifeffit"

If you do not get an error (which would probably start with "Can't locate..."), then the wrapper is installed properly.  

TODO:
----
- Modify setup.py file to check for a functioning ifeffit perl wrapper
- http://cars9.uchicago.edu/autobk/refman/node80.html

Known issues
----
- The message "Fatal Error: No absorbing atom (ipot=0) defined" probably means that the attempt at xyz conversion failed.  At this point, try running the test\_xyz\_converter.py script.
- Files with incredibly long names cause errors.  This is probably for the best (since some filesystems cannot move or delete very long names in files... Windows 7)

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
