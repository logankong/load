import os


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


clinet_ip = '172.16.2.6'
client_ip_list = get_ip(clinet_ip)

args = []
for i in range(20000):
    a = 'ip addr add ' + next(client_ip_list) + '/16 dev eth0 scope 1'
    os.system(a)
