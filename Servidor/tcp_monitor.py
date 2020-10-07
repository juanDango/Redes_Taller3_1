import socket
import struct
import textwrap

TAB_1 = '\t - '
TAB_2 = '\t\t - '
TAB_3 = '\t\t\t - '
TAB_4 = '\t\t\t\t - '

DATA_TAB_1 = '\t   '
DATA_TAB_2 = '\t\t   '
DATA_TAB_3 = '\t\t\t   '
DATA_TAB_4 = '\t\t\t\t   '

connections = {'cent': True}

def main2():
    conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
    while connections['cent']:
        raw_data, addr = conn.recvfrom(65536)
        dest_mac, src_mac, eth_proto, data = ethernet_frame(raw_data)
        if eth_proto == 8:
            (version, header_length, ttl, proto, src, target, data) = ipv4_Packet(data)

            if proto == 6:
                src_port, dest_port, sequence, acknowledgment = struct.unpack('! H H L L', data[:12])
                if src_port == 60001 and (target, dest_port) in connections:
                    connections[(target, dest_port)]['sent'] += 1
                    connections[(target, dest_port)]['bytes_sent'] += len(data)
                    if sequence != connections[(target, dest_port)]['current_SEQ']:
                        connections[(target, dest_port)]['current_SEQ'] = sequence
                        connections[(target, dest_port)]['received'] += 1
                        connections[(target, dest_port)]['bytes_received'] += len(data)
                    else:
                        connections[(target, dest_port)]['retrans'] += 1
                    #print((target, dest_port), 'SEQ:', sequence, 'ACK:', acknowledgment)

# Unpack Ethernet Frame
def ethernet_frame(data):
    dest_mac, src_mac, proto = struct.unpack('! 6s 6s H', data[:14])
    return get_mac_addr(dest_mac), get_mac_addr(src_mac), socket.htons(proto), data[14:]

    # Format MAC Address
def get_mac_addr(bytes_addr):
    bytes_str = map('{:02x}'.format, bytes_addr)
    mac_addr = ':'.join(bytes_str).upper()
    return mac_addr

# Unpack IPv4 Packets Recieved
def ipv4_Packet(data):
    version_header_len = data[0]
    version = version_header_len >> 4
    header_len = (version_header_len & 15) * 4
    ttl, proto, src, target = struct.unpack('! 8x B B 2x 4s 4s', data[:20])
    return version, header_len, ttl, proto, ipv4(src), ipv4(target), data[header_len:]

# Returns Formatted IP Address
def ipv4(addr):
    return '.'.join(map(str, addr))


# Unpacks for any ICMP Packet
def icmp_packet(data):
    icmp_type, code, checksum = struct.unpack('! B B H', data[:4])
    return icmp_type, code, checksum, data[4:]

# Unpacks for any TCP Packet
def tcp_seg(data):
    (src_port, dest_port, sequence, acknowledgenment, offset_reserv_flag) = struct.unpack('! H H L L H', data[:14])
    offset = (offset_reserv_flag >> 12) * 4
    flag_urg = (offset_reserv_flag & 32) >> 5
    flag_ack = (offset_reserv_flag & 32) >>4
    flag_psh = (offset_reserv_flag & 32) >> 3
    flag_rst = (offset_reserv_flag & 32) >> 2
    flag_syn = (offset_reserv_flag & 32) >> 1
    flag_fin = (offset_reserv_flag & 32) >> 1

    return src_port, dest_port, sequence, acknowledgenment, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin, data[offset:]


# Unpacks for any UDP Packet
def udp_seg(data):
    src_port, dest_port, size = struct.unpack('! H H 2x H', data[:8])
    return src_port, dest_port, size, data[8:]

# Formats the output line
def format_output_line(prefix, string, size=80):
    size -= len(prefix)
    if isinstance(string, bytes):
        string = ''.join(r'\x{:02x}'.format(byte) for byte in string)
        if size % 2:
            size-= 1
            return '\n'.join([prefix + line for line in textwrap.wrap(string, size)])

def addConnection(addr, port):
    connections[(addr, port)] = {
        'client': (addr, port),
        'sent': 0,
        'received': 0,
        'retrans': 0,
        'current_SEQ': -1,
        'bytes_sent': 0,
        'bytes_received': 0
    }
    print('MONITORING ADDED', addr, port)

def endConnection(addr, port):
    stats = connections.pop((addr, port), None)
    print('MONITORING ENDED', addr, port)
    print(len(connections))
    if len(connections) == 1:
        connections['cent'] = False
    return stats

#main2()