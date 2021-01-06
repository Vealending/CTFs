#!/usr/bin/env python3

import socket


TCP_IP = "fibonacci"
TCP_PORT = 7600
amount = 0

#connect to socket

def main():

    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((TCP_IP, TCP_PORT))

    for i in range(10000):
        amount = conn.recv(4096).decode("utf-8")
        print(amount)
        sendback = fibonacci_calc(int(amount[4:-2]))
        conn.send(str(sendback).encode())

#calculate fibonacci

def fibonacci_calc(terms):

    n1, n2 = 0, 1
    count = 0

    while count < terms:
        nth = n1 + n2
        n1 = n2
        n2 = nth
        count += 1
    else:
        return n1


if __name__ == "__main__":
    main()

