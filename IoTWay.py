import urequests
from crypto import AES
import binascii
import gc

IOTWAY_DEBUG = True

IOTWAY_ERROR = 2
IOTWAY_MESSAGE = 1

serverAddress = None
serverPort = None
productId = None
accessToken = None
encryptionKey = None


def IoTWayInit (*args):
    global serverAddress, serverPort, productId, accessToken, encryptionKey
    if len(args) == 5:
        serverAddress = args[0]
        serverPort = args[1]
        productId = args[2]
        accessToken = args[3]
        encryptionKey = args[4]
    elif len(args) == 4:
        serverAddress = args[0]
        serverPort = '80'
        productId = args[2]
        accessToken = args[3]
        encryptionKey = args[4]
    else:
        if IOTWAY_DEBUG:
            print ("The number of arguments for IoTWayInit must be 4 or 5")
            return

    try:
        serverPort = int(serverPort)
    except ValueError:
        print ("The serverPort argument must be a valid port")
        return

    try:
        x = encryptionKey.strip()
        x = x.replace(" ", "")
        encryptionKey = [i+j for i,j in zip(x[::2], x[1::2])]
        
        if (len(encryptionKey) != 16):
            print ("The encryptionKey argument must have 16 groups of hex chars")
            return

        encryptionKey = bytes(map(lambda x : int(x,16), encryptionKey))


    except Exception as e:
        print (e)
        print ("The encryptionKey argument is in a wrong format")
        return

    

def send(clearSend):
    key = encryptionKey
    iv = bytes(map(ord, accessToken[0:16]))

    if len(clearSend) % 16 != 0:
        pad = 16 - (len(clearSend) % 16)
        clearSend = clearSend + (pad * chr(pad)) #pad PKCS#7

    cryptor = AES(key, AES.MODE_CBC, iv)
    ciphertext = cryptor.encrypt(clearSend)

    toSend = binascii.b2a_base64(ciphertext)[:-1]

    a = urequests.post("http://" + serverAddress + ':' + str(serverPort) + '/exchange', headers = {
        "Connection": "close",
        "Content-Type": "text/plain",
        "User-Agent": "iotway-product",
        "Host": serverAddress,
        "Authorization": "Bearer " + productId
    }, data = toSend)
    

def IoTWayMessage (message, ty = IOTWAY_MESSAGE):
    if ty == IOTWAY_MESSAGE:
        c = 'c'
    elif ty == IOTWAY_ERROR:
        c = 'd'

    clearSend = b"w:%s\nt:%s\nn:%d\nm:%s" % (c, accessToken, 100, message)
    send(clearSend)

def IoTWayError (message):
    IoTWayMessage(message, IOTWAY_ERROR)

def IoTWayStatus ():
    gc.collect() ; (alloc, free) = (gc.mem_alloc(), gc.mem_free()) # one shot
    clearSend = b"w:b\nt:%s\ns:%s\nn:%d\ne:%d\nf:%d\nc:%d" % (accessToken, "on", 100, alloc, alloc+free, 100)
    send(clearSend)
    
def IoTWaySignal(signal, values):
    IoTWaySignals(signal, values)

def IoTWaySignals (signals, values):
    if isinstance(signals, list) and isinstance(values, list) and len(signals) == len(values):
        pass
    elif isinstance(signals, str) and isinstance(values, str):
        signals = [signals]
        values = [values]
    else:
        print ("The signals and values arguments are in a wrong format")
        return

    clearSend = b"w:a\nt:%s\na:%s\nn:%d\ns:\n" % (accessToken, "", 100) 
    for i in range(len(signals)):
        clearSend += (" %s:%s\n" % (signals[i], values[i]))
    
    send(clearSend)

