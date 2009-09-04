#!/usr/bin/python
#
# Check debug symbol files for inconsistency between their CRC and
# what the parent library thinks it's debug libraries CRC should be.
#

import os
import binascii
import re
import commands
import string

debug_path="/usr/lib/debug"

def check_symbol_file(file):
    # We now need to calculate the path the debug library is refering to
    target_file = re.sub(debug_path, "", file)
    if os.path.isfile(target_file):
        # OK, we have a match. Calculate the CRC of the debug library
        data = open(file).read()
        crc = binascii.crc32(data)
        crc = crc % 2**32  

        # Now find out what the parent file thinks the CRC should be
        obj_output = commands.getoutput("objdump -s -j .gnu_debuglink "+target_file)
        # The last 8 hex digits are the (byte reversed) CRC
        bytes = re.findall("[0-9a-f]{8}", obj_output)
        obj_crc = bytes[len(bytes)-1] # I'm sure there is a more concise way
        swap_crc=[]
        for i in range(0, len(obj_crc), 2):
            swap_crc.insert(0, obj_crc[i:i+2])
        real_crc = string.atol(''.join(swap_crc), 16)

        # Finally complain if the CRCs do not match
        if real_crc != crc:
            print "debug_file: %s has CRC of %X" % (file, crc)
            print "library_file: %s thinks CRC is %X" % (target_file, real_crc)

def check_dir(dir):
    for e in os.listdir(dir):
        path = dir+"/"+e
        if os.path.isdir(path):
            check_dir(path)
        else:
            print "checking: %s" % (path)
            check_symbol_file(path)
    

check_dir(debug_path)

