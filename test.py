from bluepy.btle import Scanner, DefaultDelegate, Peripheral, AssignedNumbers
import threading

class NotificationDelegate(DefaultDelegate):

    def __init__(self, number):
        DefaultDelegate.__init__(self)
        self.number = number

    def handleNotification(self, cHandle, data):
        print 'Notification:\nConnection:'+str(self.number)+'\nHandler:'+str(cHandle)+'\nMsg:'+data

if __name__=="__main__":
    cccid = AssignedNumbers.client_characteristic_configuration
    hrmid = AssignedNumbers.heart_rate
    hrmmid = AssignedNumbers.heart_rate_measurement
print("AssignedNumbers")
print(str(hrmid))
bt_addrs = ['50:8c:b1:6a:02:f7', '50:8c:b1:69:f9:45', 'f9:eb:97:ee:2f:88']
connections = []
connection_threads = []
scanner = Scanner(0)

class ConnectionHandlerThread (threading.Thread):
    def __init__(self, connection_index):
        threading.Thread.__init__(self)
        self.connection_index = connection_index

    def run(self):

        connection = connections[self.connection_index]
        connection.setDelegate(NotificationDelegate(self.connection_index))
        while True:
            connection.writeCharacteristic(18, 'Data')
            if connection.waitForNotifications(1):
                connection.writeCharacteristic(18, 'Thank you for the notification!')

while True:

    print'Connected: '+str(len(connection_threads))
    print 'Scanning...'
    devices = scanner.scan(2)
    for d in devices:
        print(d.addr)
        if d.addr in bt_addrs:
            p = Peripheral(d)

            connections.append(p)
            t = ConnectionHandlerThread(len(connections)-1)
            t.start()
            connection_threads.append(t)
