#!/usr/bin/env python
import sys
from run_script import update_file;
print sys.argv
update_file(*sys.argv[1:])
