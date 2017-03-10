# vmware_scanner
VMware Scanner - Easy find all running VMware solutions on your network

Using the VMware API (SOAP Based), this simple python script will query any server on the specified network, returning (if VMware product) the product name, version and build number.


Example:
C:\Python33>python scan_v2.py
Scanner client started...
100.0% - found: 0
57.8% - found: 0
57.0% - found: 0
20.0% - found: 0
192.168.1.207 - VMware ESXi 5.1.0 build-1065491
192.168.1.217 - VMware ESXi 5.1.0 build-1065491
13.7% - found: 2
13.7% - found: 2
Done scanning
total found: 2
done

