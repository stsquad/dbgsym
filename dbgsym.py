#!/usr/bin/python
#
# Check debug symbol files for inconsistency

import os
import binascii
import re

debug_path="/usr/lib/debug"

def check_symbol_file(file):
    # First calculate it's CRC
    data = open(file).read()
    crc = binascii.crc32(data)
    print "CRC is %X" % (crc)

    # objdump -s -j .gnu_debuglink /usr/lib/libattr.so
    # We now need to calculate the path the debug library is refering to
    target_file = re.sub(debug_path, "", file)
    if os.path.isfile(target_file):
        print "found: %s" % (target_path)
    

def check_dir(dir):
    for e in os.listdir(dir):
        path = dir+"/"+e
        if os.path.isdir(path):
            check_dir(path)
        else:
            print "checking: %s" % (path)
            check_symbol_file(path)
    

check_dir(debug_path)

