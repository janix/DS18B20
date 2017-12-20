#!/usr/bin/python -u

# add to /etc/snmp/snmpd.conf
# pass_persist .1.3.6.1.2.1.25.1.8 /path/to/sensors.py


import sys
lista = [
"/sys/bus/w1/devices/28-03146a7692ff/w1_slave",
"/sys/bus/w1/devices/28-03146a78d9ff/w1_slave",
"/sys/bus/w1/devices/28-03146a777fff/w1_slave",
"/sys/bus/w1/devices/28-03146aaf1fff/w1_slave",
"/sys/bus/w1/devices/28-051685e09cff/w1_slave",
"/sys/bus/w1/devices/28-0416747c6cff/w1_slave",
"/sys/bus/w1/devices/28-0516810060ff/w1_slave"

]
sensors = {}

def iter():
    i = 1

    for item in lista:
        tempfile = open(item)
        thetext = tempfile.read()
        tempfile.close()
        tempdata = thetext.split("\n")[1].split(" ")[9]
        temperature = int(tempdata[2:])
        #ignore sensor errors
        if temperature < 10000000:
            sensors[i] = temperature
#        print sensors[i]
        i += 1

import snmp_passpersist as snmp
OID_BASE=".1.3.6.1.2.1.25.1.8"


def update():
    global pp
    iter()
    #OID == .1.3.6.1.2.1.25.1.8.3
    pp.add_int('3',sensors[1])
    #OID == .1.3.6.1.2.1.25.1.8.4
    pp.add_int('4',sensors[2])
    #...
    pp.add_int('5',sensors[3])
    pp.add_int('6',sensors[4])
    pp.add_int('9',sensors[5])
    pp.add_int('10',sensors[6])
    pp.add_int('11',sensors[7])


try:
    pp=snmp.PassPersist(OID_BASE)
    pp.start(update,30)

except KeyboardInterrupt:
    print "Exiting on user request."
    sys.exit(0)
