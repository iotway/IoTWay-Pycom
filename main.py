from network import WLAN
import machine
import time
from IoTWay import IoTWayInit, IoTWaySignal, IoTWaySignals, IoTWayStatus, IoTWayMessage, IoTWayError

wlan = WLAN(mode=WLAN.STA)

SSID = 'your-ssid'
password = 'your-password'

nets = wlan.scan()
for net in nets:
    if net.ssid == SSID:
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, password), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        break

else:
    print ("Network not found")

#Arguments in order : Proxy url, Port, ProductId, ProductToken (Short Token, 64 chars), Product Symetric Key (AES)
IoTWayInit("proxy.iotway.net", 80, "pycomBoardUniqueIdFromStudioIotWayNet", "ThisIsTheTokenForTheProductThatYouTakeFromStudioIotWayNetxxxxxxx", "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00")

#example status sending
#IoTWayStatus()

#put delay because the server rejects requests that are made too often
#time.sleep(10)

#example signal sending
#IoTWaySignal ("signalName", "Value")
  
#put delay because the server rejects requests that are made too often
#time.sleep(10)

#example message sending
#IoTWayMessage ("This message will be sent to server");
  
#put delay because the server rejects requests that are made too often
#time.sleep(10)

#example message sending
#IoTWayError ("This message will be sent to server as error");

#put delay because the server rejects requests that are made too often
#time.sleep(10)