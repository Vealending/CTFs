From reading the packets there was some obvious DNS tunneling going on.
Used the following to extract all the query names, prepended with their timestamps for easier sorting:

```python
import pyshark
  
pcap_file = pyshark.FileCapture("C:\\Users\\<REDACTED>\\Downloads\\forensics_trick_or_breach\\capture.pcap")
dns_names = set()
  
for p in pcap_file:
  
	try:
		dns_names.add(p.sniff_timestamp + " - " + p.dns.qry_name)
	except Exception as e:
		print(e)
		pass

for name in dns_names:
    print(name)
```

Cleaned the output using CyberChef's "Sort" and "Replace" recipes.
The magic bytes ("50 4B 03 04") indicated a KZIP archive.
Used the "From Hex" recipe and saved the output to a file. Tried extracting it, but to no avail.
Saw that the magic bytes for .xlsx files were ("50 4B 03 04 14 00 06 00"), so I renamed the file to .xlsx and tried opening it using Excel 2016.
It said the file was damaged and if I wanted to repair it.
Clicking yes reveals the flag in one of the cells on the spreadsheet.