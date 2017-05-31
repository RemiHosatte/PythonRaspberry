from bluepy.btle import Peripheral, ADDR_TYPE_RANDOM, AssignedNumbers

import time
print("Start")
class HRM(Peripheral):
    def __init__(self, addr):
        Peripheral.__init__(self, addr, addrType=ADDR_TYPE_RANDOM)

if __name__=="__main__":
    cccid = AssignedNumbers.client_characteristic_configuration
    hrmid = AssignedNumbers.heart_rate
    hrmmid = AssignedNumbers.heart_rate_measurement

    hrm = None
    try:
        hrm = HRM('F9:EB:97:EE:2F:88')
        #Montre rouge EF:77:CA:CD:62:5F
        #Montre bleu F9:EB:97:EE:2F:88

        service, = [s for s in hrm.getServices() if s.uuid==hrmid]
        ccc, = service.getCharacteristics(forUUID=str(hrmmid))

        if 0: # This doesn't work
            ccc.write('\1\0')

        else:
            desc = hrm.getDescriptors(service.hndStart,
                                      service.hndEnd)
            d, = [d for d in desc if d.uuid==cccid]

            hrm.writeCharacteristic(d.handle, '\1\0')

        t0=time.time()
        def print_hr(cHandle, data):

            bpm = ord(data[1])
            rr = ord(data[2])
            rr2 = ord(data[3])

            rr = '{:08b}'.format(rr)
            rr2 ='{:08b}'.format(rr2)
            rrInMs = int(rr2+rr,2)
            print "RR in ms: "+str(rrInMs)
            print "BPM: " +str(bpm)
        hrm.delegate.handleNotification = print_hr

        for x in range(10000):
            hrm.waitForNotifications(3.)

    finally:
        if hrm:
            hrm.disconnect()
