##Usage:
./unzip.py master.zip 
or
python3 unzip.py master.zip


#!/usr/bin/env python3
import sys
from zipfile import PyZipFile
for zip_file in sys.argv[1:]:
    pzf = PyZipFile(zip_file)
    pzf.extractall()
