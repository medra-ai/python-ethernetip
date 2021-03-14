import ethernetip


def test_ports():
    assert ethernetip.ENIP_TCP_PORT == 44818, "Someone stole the specified port"
