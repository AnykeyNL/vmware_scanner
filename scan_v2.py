#!pyhton3
# VMware Scanner v2.02 - March 2017
# Written by the.anykey@gmail.com
#
# Feel free to use in any way you like

import http.client
import threading
import time
import ssl
from queue import Queue

scanTimeout = 5           # Timeout per connection in seconds
maxThreads = 100          # max threads for scanning
statusUpdateFrequency = 2 # show every X seconds on screen the status
found = 0

soapmsg_start = "<soapenv:Body>"
soapmsg_ends = "</soapenv:Body>"
fullname_start = "<fullName>"
fullname_ends = "</fullName>"


def CheckServer(ipaddr):
    global found
    IPaddress = ipaddr

    soapmsg = '<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><soapenv:Body><RetrieveServiceContent xmlns="urn:vim25"><_this type="ServiceInstance">ServiceInstance</_this></RetrieveServiceContent></soapenv:Body></soapenv:Envelope>'
    #conn = http.client.HTTPSConnection(IPaddress, timeout=scanTimeout, context=ssl._create_unverified_context()) # use for python 3.6+
    conn = http.client.HTTPSConnection(IPaddress, timeout=scanTimeout)
    params = soapmsg
    headers = {"Content-type": "application/soap+xml"}

    try:
        conn.request("POST", "/sdk/vimService", params, headers)
        r1 = conn.getresponse()
        data = r1.read()
        datas = data.decode(encoding='utf-8')
        if "rootFolder" in datas:
            soapbody = ExtractSoapMsg(datas)
            found = found + 1
            dumpdata(ipaddr, ExtractFullName(soapbody))
    except:
        return


def ExtractSoapMsg(soapmsg):
    beg = soapmsg.find(soapmsg_start) + len(soapmsg_start) + 1
    ends = soapmsg.find(soapmsg_ends) - 1
    soapbody = soapmsg[beg:ends]
    return soapbody


def ExtractFullName(soapbody):
    beg = soapbody.find(fullname_start) + len(fullname_start)
    ends = soapbody.find(fullname_ends)
    fullname = soapbody[beg:ends]
    return fullname


def worker():
    while True:
        ipaddr = q.get()
        CheckServer(ipaddr)
        q.task_done()


def StartScanJob2(a, b):
    for c in range(254):
         for d in range(254):
            ipaddr = str(a) + "." + str(b) + "." + str(c + 1) + "." + str(d + 1)
            q.put(ipaddr)
    WaitCompletion()

def StartScanJob3(a, b, c):
    for d in range(254):
            ipaddr = str(a) + "." + str(b) + "." + str(c) + "." + str(d + 1)
            q.put(ipaddr)
    WaitCompletion()

def WaitCompletion():
    totalQ = q.qsize()
    while (q.qsize() > 0):
        print (str(int((q.qsize()*100)/(totalQ)*10)/10) + "% - found: " + str(found) )
        time.sleep(statusUpdateFrequency)

    q.join()

    print("Done scanning")
    print("total found: " + str(found))

def dumpdata(hostip, version):
    print (hostip + " - " + version)


print("Scanner client started...")
lock = threading.Lock()
q = Queue()

for i in range(maxThreads):
    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()



#------ Start Scanning


StartScanJob3(192, 168, 1)

print ("done")
