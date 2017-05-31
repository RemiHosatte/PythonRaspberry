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
        hrm = HRM('EF:77:CA:CD:62:5F')
        //Montre rouge EF:77:CA:CD:62:5F
        //Montre bleu F9:EB:97:EE:2F:88

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
            print bpm,"%.2f"%(time.time()-t0)
        hrm.delegate.handleNotification = print_hr

        for x in range(100):
            hrm.waitForNotifications(3.)

    finally:
        if hrm:
            hrm.disconnect()
