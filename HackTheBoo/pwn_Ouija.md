We are given a binary that prints the flag, but does so incredibly slowly.
It uses sleep() to wait between each action.
Using LD_PRELOAD, we can make sleep() do nothing:

**nosleep.c**
```c
int sleep(unsigned int seconds)
{
    return 0;
}
```

**Compile as library**
```sh
gcc -o libnosleep.so -shared nosleep.c -fpic
```

**Run the binary:**
```sh
LD_PRELOAD=./libnosleep.so ./ouija
```

The process finishes running in less than a second, and we get our flag after cleaning the output a little.
