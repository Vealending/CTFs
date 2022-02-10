#!/usr/bin/env python3

import socket
import struct
import select
import threading
import multiprocessing
import time

TCP_IP = "127.0.0.1"
TCP_PORT = 10015
rlist = []
bArray = bytearray()

def main():

    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    conn.connect((TCP_IP, TCP_PORT))
    print(conn.recv(4096).decode("utf-8"))

    sockets = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) for _ in range(10)]

    for s in sockets:
        s.connect((TCP_IP, TCP_PORT))

    print(conn.recv(4096).decode("utf-8"))

    for s in sockets:
        rlist.append(int.from_bytes(s.recv(32), "big"))

    conn.send(struct.pack('>i', sum(rlist),))
    print(conn.recv(4096).decode("utf-8"))

    rlist.clear()

    for i in range(450):

        rs, ws, es = select.select(sockets, [], [])

        for s in rs:
            data = s.recv(4096)
            if not data:
                print("Empty")
                break
            else:
                rlist.append(data)

    print(b''.join(rlist).decode("utf-8"))

