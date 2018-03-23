# enum-tools
Random quick scripts to enumerate information assembled for various reasons. No error checking, prone to random failure. Will update if I continue to use them regularly:

Enumvariation - quick tool to request a url with various user agents and display the size of responses, useful for seeing if sites behave differently with different user agents, e.g. some sites do not display anything unless sent an IE header.
Used with enumvariation.py -u <url>

GetApi.py - Quick and dirty tool to request asname, whoisdesc and bgpinfo. Useful for seeing who owns an IP range and the CIDR of it.
Used with GetApi.py -f <iplist.txt>
