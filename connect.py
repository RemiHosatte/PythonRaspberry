#!/usr/bin/env python

from bluepy.btle import Scanner, DefaultDelegate, Peripheral

class ScanDelegate(DefaultDelegate):
	def __init__(self):
		DefaultDelegate.__init__(self)

	def handleDiscovery(self, dev, isNewDev, isNewData):
		if isNewDev:
			pass
		#elif isNewData:
		#print "Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi)
		#print dev.getScanData()

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(2.0)

for dev in devices:

		print "Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi)
		for (adtype, desc, value) in dev.getScanData():
				if dev.addr == "f9:eb:97:ee:2f:88":
					p = Peripheral("f9:eb:97:ee:2f:88")
					#print(p.getServices())
