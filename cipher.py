#!/usr/bin/env python3

import numpy
from ctypes import c_uint32 as unsigned_int32

def main():

    Pin = [1, 2, 5, 2]
    Pin_byte_array = bytearray(Pin)

    r = Obfuscator(Pin_byte_array)
    print(r)

    i = 48
    i2 = 16

def Obfuscator(byte_array):

    cArr = numpy.empty(len(byte_array) * 2, dtype=object)

    for i in byte_array:
        i2 = byte_array[i] & 255
        i3 = i * 2
        cArr2 = "0123456789ABCDEF"
        cArr[i3] = cArr2[unsigned_int32(i2).value >> 4]
        cArr[i3 + 1] = cArr2[i2 & 15]

        return cArr
    