import subprocess
import time

def brute_force():

	found = False
	pin = ""
	i = 0

	while not found:

		longest_time = 0
		longest_number = 0

		for i in range(0,10):

			time_used, stdout = test_pin(pin + str(i))

			if time_used > longest_time:
				longest_time = time_used
				longest_number = i

		pin += str(longest_number)
		print("Current pin:", pin)

		if not "denied" in stdout:
			print("Correct pin is:", pin)
			print(stdout)
			found = True

def test_pin(pin):

	test = str(pin).ljust(8, "0")

	start_time = time.time()
	p = subprocess.Popen(["/home/kali/picoCTF/pin_checker"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	stdout = p.communicate(input = test.encode())[0].decode()
	time_used = time.time() - start_time

	print(test, time_used)

	return time_used, stdout

if __name__ == "__main__":

	brute_force()