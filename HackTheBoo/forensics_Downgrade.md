Fairly straight forward. We are given lots of Windows event log files, and need to answer questions over a network connection.
The questions were very leading. The main problem was that the time/date had to be in UTC.

```
Which event log contains information about logon and logoff events? (for example: Setup)
> Security
[+] Correct!

What is the event id for logs for a successful logon to a local computer? (for example: 1337)
> 4624
[+] Correct!

Which is the default Active Directory authentication protocol? (for example: http)
> ldap
[-] Wrong Answer.
Which is the default Active Directory authentication protocol? (for example: http)

> kerberos
[+] Correct!

Looking at all the logon events, what is the AuthPackage that stands out as different from all the rest? (for example: http)
> NTLM
[+] Correct!

What is the timestamp of the suspicious login (yyyy-MM-ddTHH:mm:ss) UTC? (for example, 2021-10-10T08:23:12)
> 2022-09-28T13:10:57
[+] Correct!

[+] Here is the flag: HTB{4n0th3r_d4y_4n0th3r_d0wngr4d3...}
```