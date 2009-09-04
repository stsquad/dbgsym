dbgsym.py - a debug symbols integrity checker.

This utility is a simple little script to check that a debug files
CRCs match those of the binary it is there for. I wrote it to see if
any other binaries on my system suffered the same problem as seen in
bug:

https://bugs.launchpad.net/ubuntu/+source/cairo/+bug/415424

But in my experimentation I found not. Still the script may be useful
to other people so I thought I'd better mention what it did.

usage:

  ./dbgsym.py

And see if it complains about anything
