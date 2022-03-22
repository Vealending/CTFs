import codecs

usernames = open("usernames.txt").read().split()
passwords = open("passwords.txt").read().split()
line = 0

for user in usernames:
	if "cultiris" in user:
		break
	line += 1

print("cultiris found at line", line)
print("Their password is", passwords[line])
print("Flag is", codecs.decode(passwords[line], 'rot_13'))