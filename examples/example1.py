import ethernetip
import random
import socket
import struct
import time


def main():
    hostname = "192.168.1.32"
    broadcast = "192.168.255.255"
    inputsize = 1
    outputsize = 1
    EIP = ethernetip.EtherNetIP(hostname)
    C1 = EIP.explicit_conn(hostname)

    listOfNodes = C1.scanNetwork(broadcast, 5)
    print("Found ", len(listOfNodes), " nodes")
    for node in listOfNodes:
        name = node.product_name.decode()
        sockinfo = ethernetip.SocketAddressInfo(node.socket_addr)
        ip = socket.inet_ntoa(struct.pack("!I", sockinfo.sin_addr))
        print(ip, " - ", name)

    pkt = C1.listID()
    if pkt is not None:
        print("Product name: ", pkt.product_name.decode())

    pkt = C1.listServices()
    print("ListServices:", str(pkt))

    # read input size from global system object (obj 0x84, attr 4)
    r = C1.getAttrSingle(0x84, 1, 4)
    if 0 == r[0]:
        print("Read CPX input size from terminal success (data: " + str(r[1]) + ")")
        inputsize = struct.unpack("B", r[1])[0]

    # read output size from global system object (obj 0x84, attr 5)
    r = C1.getAttrSingle(0x84, 1, 5)
    if 0 == r[0]:
        print("Read CPX output size from terminal sucess (data: " + str(r[1]) + ")")
        outputsize = struct.unpack("B", r[1])[0]

    # configure i/o
    print("Configure with {0} bytes input and {1} bytes output".format(inputsize, outputsize))
    EIP.registerAssembly(ethernetip.EtherNetIP.ENIP_IO_TYPE_INPUT, inputsize, 101, C1)
    EIP.registerAssembly(ethernetip.EtherNetIP.ENIP_IO_TYPE_OUTPUT, outputsize, 100, C1)
    EIP.startIO()

    C1.registerSession()

    C1.setAttrSingle(ethernetip.CIP_OBJ_TCPIP, 1, 6, "fbxxx")

    for i in range(1, 8):
        r = C1.getAttrSingle(ethernetip.CIP_OBJ_IDENTITY, 1, i)
        if 0 == r[0]:
            print("read ok attr (" + str(i) + ") data: " + str(r[1]))
        else:
            print("Err: " + str(r[0]))

    C1.sendFwdOpenReq(101, 100, 1)
    C1.produce()

    while True:
        try:
            time.sleep(0.2)
            C1.outAssem[random.randint(0, len(C1.outAssem) - 1)] = True
            C1.outAssem[random.randint(0, len(C1.outAssem) - 1)] = False
        except KeyboardInterrupt:
            break
    C1.stopProduce()
    C1.sendFwdCloseReq(101, 100, 1)
    EIP.stopIO()


if __name__ == "__main__":
    main()
