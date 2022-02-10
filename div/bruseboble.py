for i in range(100):

	svar = ""

	if not i % 3:
		svar += "bruse"

	if not i % 5:
		svar += "boble"

	print(svar or i)