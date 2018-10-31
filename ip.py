import struct
import binascii
import random
import sys


def get_ip(start='1.1.1.1'):
        starts = start.split('.')
        A = int(starts[0])
        B = int(starts[1])
        C = int(starts[2])
        D = int(starts[3])
        for A in range(A, 256):
            for B in range(B, 256):
                for C in range(C, 256):
                    for D in range(D, 255):
                        ip = "%d.%d.%d.%d" % (A, B, C, D)
                        yield ip
                    D = 1
                C = 0
            B = 0

def randomMAC():
    mac = [0x52, 0x54, 0x00,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))


def macs2a(mac):
    dict = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5,
            '6': 6, '7': 7, '8': 8, '9': 9, 'a': 10, 'b': 11,
            'c': 12, 'd': 13, 'e': 14, 'f': 15}

    mac = mac.lower()
    tmp = mac.split(':')
    if sys.version_info < (3, 4):
        res = ''
        for i in range(len(tmp)):
            uc = struct.pack('B', 16 * dict[tmp[i][0]] + dict[tmp[i][1]])
            res = res + uc
    else:
        res = ''.encode(encoding="utf-8")
        for i in range(len(tmp)):
            uc = struct.pack('B', 16 * dict[tmp[i][0]] + dict[tmp[i][1]])
            res = res + uc
    return res


def macAdd(mac, step=1):
    mac1, mac2 = struct.unpack('!HL', mac)
    mac2 = mac2 + step
    return struct.pack("!HL", mac1, mac2)


def macSelfAdd(mac, num=0, step=1):
    macTmp = macs2a(mac)
    e = []
    for i in range(num):
        macTmp = macAdd(macTmp, step)
        if sys.version_info < (3, 4):
            macTmp = macAdd(macTmp, step)
            macStr = binascii.b2a_hex(macTmp)
            new_mac = macStr[0:2] + ":" + macStr[2:4] + ":" + macStr[4:6] + \
                ":" + macStr[6:8] + ":" + macStr[8:10] + ":" + macStr[10:12]
            e.append(new_mac)
        else:
            mac0x = binascii.b2a_hex(macTmp)
            macStr = str(bytes(mac0x))[2:-1]
            new_mac = macStr[0:2] + ":" + macStr[2:4] + ":" + macStr[4:6] + \
                ":" + macStr[6:8] + ":" + macStr[8:10] + ":" + macStr[10:12]
            e.append(new_mac)
    return e


def get_port(num, port=9101):
    for i in range(num):
        yield i + port


if __name__ == '__main__':
    # t = get_port(9101)
    for i in get_port(5):
        print(i, ":"),
    # a = macSelfAdd('00:00:00:00:00:01', 1000, 30000)
    # print(sys.getsizeof(a))
    # print(a)
