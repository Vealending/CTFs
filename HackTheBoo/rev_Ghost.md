Opening the binary in IDA reveals this interesting part:

```c
  s = malloc(0x29uLL);
  memset(s, 0, 0x29uLL);
  for ( i = 0; i <= 0x27; ++i )
    *(s + i) = _[i] ^ 0x13;
  return s;
}
```

Something is being XOR'ed with 0x13.
Double clicking the `_[i]` takes us to a byte array stored in .rodata

```c
.rodata:0000000000002020 _               db 5Bh, 47h, 51h, 68h, 7Bh, 27h, 66h, 7Dh, 67h, 20h, 77h
.rodata:0000000000002020                                         ; DATA XREF: get_flag+3A↑o
.rodata:0000000000002020                 db 4Ch, 71h, 6Ah, 4Ch, 67h, 7Bh, 20h, 4Ch, 74h, 7Bh, 23h
.rodata:0000000000002020                 db 60h, 67h, 26h, 4Ch, 23h, 75h, 4Ch, 70h, 67h, 75h, 26h
.rodata:0000000000002020                 db 4Ch, 63h, 27h, 26h, 67h, 32h, 6Eh
```

Used CyberChef to reverse the XOR:

```
5Bh, 47h, 51h, 68h, 7Bh, 27h, 66h, 7Dh, 67h, 20h, 77h
4Ch, 71h, 6Ah, 4Ch, 67h, 7Bh, 20h, 4Ch, 74h, 7Bh, 23h
60h, 67h, 26h, 4Ch, 23h, 75h, 4Ch, 70h, 67h, 75h, 26h
4Ch, 63h, 27h, 26h, 67h, 32h, 6Eh

	|
	V

From Hex

	|
	V

[GQh{'f}g wLqjLg{ Lt{#`g&L#uLpgu&Lc'&g2n

	|
	V

XOR (key: 0x13)

	|
	V

HTB{h4unt3d_by_th3_gh0st5_0f_ctf5_p45t!}
```

```txt
https://gchq.github.io/CyberChef/#recipe=From_Hex('Auto')XOR(%7B'option':'Hex','string':'0x13'%7D,'Standard',false)&input=NUJoLCA0N2gsIDUxaCwgNjhoLCA3QmgsIDI3aCwgNjZoLCA3RGgsIDY3aCwgMjBoLCA3N2gKNENoLCA3MWgsIDZBaCwgNENoLCA2N2gsIDdCaCwgMjBoLCA0Q2gsIDc0aCwgN0JoLCAyM2gKNjBoLCA2N2gsIDI2aCwgNENoLCAyM2gsIDc1aCwgNENoLCA3MGgsIDY3aCwgNzVoLCAyNmgKNENoLCA2M2gsIDI3aCwgMjZoLCA2N2gsIDMyaCwgNkVo
```