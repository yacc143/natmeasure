This is a tiny program that demonstrates the issue with the UPC
Technicolor "Modem/Router" TC-7200U as deployed by UPC Austria.

It measures how long the Technicolor TCP/IP stack keeps the
information about a TCP connection alive.

You need a ssh server that you can login via public key
authentication. ssh has been choosen to minimize measurment
interference by native timeouts in the service. 

The measurement is done my starting ssh as many time as necessary, and
making it output (from the remote host) a START line, make it wait the
given amount of time and then an OK line.

With a correctly working TCP/IP stack this should just work trivially
even for long wait periods.

For analysing the output of the script, the following commandline is
useful:

awk ' /START|OK/ { print $7 " " $8 } ' REPORTFILE  | sort -n

In my case I can reliably reproduce that connections get droppeded
SILENTLY!!! after being about 330 seconds idle. This means that
neither the client nore the server discover that the connection is
gone till after they've tried to send some data.
