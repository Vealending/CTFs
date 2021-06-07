#!/usr/bin/env python3

import socket
import struct

TCP_IP = "transfer"
TCP_PORT = 1334

magic_byte = bytearray("FILE", "utf-8")
seq_num = bytearray(8)
instruction = bytearray(1)
length = bytearray(8)

def main():

    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((TCP_IP, TCP_PORT))

    instruction = b'00000000'

    packet = magic_byte, seq_num, instruction, length

    #conn.send(packet.encode())
    conn.send(packet)
    print(recv(conn))



def recv(conn):
    raw_message = recvall(conn, 20)
    if not raw_message:
        return None
    msg_length = struct.unpack()
    return recvall(conn, msg_length)

def recvall(conn, n):
    data = bytearray()
    while len(data) < n:
        packet = conn.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data


if __name__ == "__main__":
        main()