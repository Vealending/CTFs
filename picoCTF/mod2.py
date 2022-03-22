flag = "268 413 110 190 426 419 108 229 310 379 323 373 385 236 92 96 169 321 284 185 154 137 186".split()
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_" # 1-26 are the alphabet, 27-36 are the decimal digits, and 37 is an underscore.

for n in flag:
	print(alphabet[pow(int(n), -1, 41) - 1], end="")