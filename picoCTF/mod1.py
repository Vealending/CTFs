flag = "54 396 131 198 225 258 87 258 128 211 57 235 114 258 144 220 39 175 330 338 297 288 ".split()
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"

for n in flag:
	print(alphabet[int(n) % 37], end="")