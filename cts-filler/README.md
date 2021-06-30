# Simple port filler

The reason for this is to keep all ports occupied, so a simple port scan won't
reveal the presence of a (virtual) transmitter. Of course one could fingerprint
the data coming out of each port and figure out which one is transmitting. To
counter that, simply create a random, but legitimate-looking, signal and stream
it onto all the ports (except those used for the actual challenges).
