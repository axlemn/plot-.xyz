Description
===========
monitors a directory for changes to or new .xyz files and then runs various processing tools on them.  

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
To use, run "python monitor\_changes.py" .  May also give the name of an alternate directory to monitor.  

TODO
====
- Modify setup.py file 
------------ Add feff processing and averaging
- Include testfiles
- Run atoms and feff6

Known bugs
=====
- Repetition of processing when an old file is updated in Vim

Changelog 
==========
- Deleted any use of a timestamp file, replacing it with an instance of watchdog.  

- Changed output files
- Modified checks to the .xyz file
