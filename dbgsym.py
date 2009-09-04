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
import getopt,sys

debug_path="/usr/lib/debug"
try_alt=False

def compare_crcs(debug_file, actual_file, verbose=False):
    # Calculate the CRC of the debug file
    data = open(debug_file).read()
    debug_crc = binascii.crc32(data)
    debug_crc = debug_crc % 2**32  # force to be signed

    # Extract the CRC from the actual file
    obj_output = commands.getoutput("objdump -s -j .gnu_debuglink "+actual_file)

    # The last 8 hex digits are the (byte reversed) CRC
    bytes = re.findall("[0-9a-f]{8}", obj_output)
    obj_crc = bytes[len(bytes)-1] # I'm sure there is a more concise way
    swap_crc=[]
    for i in range(0, len(obj_crc), 2):
        swap_crc.insert(0, obj_crc[i:i+2])
    real_crc = string.atol(''.join(swap_crc), 16)

    # Finally complain if the CRCs do not match
    if (real_crc != debug_crc) or verbose:
        print "debug_file: %s has CRC of %X" % (debug_file, debug_crc)
        print "actual_file: %s thinks CRC should be %X" % (actual_file, real_crc)
        
    

def process_debug_file(debug_file):
    # We now need to calculate the path the debug library is refering to
    target_file = re.sub(debug_path, "", debug_file)
    if os.path.isfile(target_file):
        compare_crcs(debug_file, target_file)
    else:
        print "couldn't find paired library for: %s" % (debug_file)
        if try_alt:
            # try alternatives, this is usually something like /usr/lib/debug/file.so
            for f in ("/lib"+target_file, "/usr/lib"+target_file, "/usr/bin"+target_file):
                if os.path.isfile(f):
                    print "trying alt: %s" % (f)
                    compare_crcs(debug_file, f, True)

def check_dir(dir):
    for e in os.listdir(dir):
        path = dir+"/"+e
        if os.path.isdir(path):
            check_dir(path)
        else:
            process_debug_file(path)

def usage():
    print "dbgsym.py [-a] [-d|--debug_root=/path/to/debug/dir] [-f|--file=/path/to/debug/file]"
    print "  -a,               : try alternate paths if matching library not found"
    print "  -d, --debug_root  : use different root (default %s)" % (debug_path)
    print "  -f, --file        : just check one debug file"
    sys.exit(1)
            
# Start of code
if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ad:f:", ["debug_root=", "file="])
    except getopt.GetoptError, err:
        usage()

    for o,a in opts:
        if o in ("-a"):
            try_alt=True
        if o in ("-d", "--debug_root"):
            debug_path=a
        if o in ("-f", "--file"):
            # do one file
            process_debug_file(a)
            exit(0)

    # Start going through the debug dir
    check_dir(debug_path)

