Opening the binary in IDA, we can see that it's capable of sending/receiving AES 256 CBC encrypted data.
The IV and key are in plain text, so we can decrypt what was sent.

Open the trace.pcap file, and find the packet with 32 bytes of data.
Right click the data section, and choose "Export Packet Bytes".
Save to a file.

Open the file in CyberChef, and input the IV and key we found earlier in the AES Decrypt recipe:
This gives us the string `HTB{vryS3CuR3_F1L3_TR4nsf3r}`

https://gchq.github.io/CyberChef/#recipe=AES_Decrypt(%7B'option':'UTF8','string':'supersecretkeyusedforencryption!'%7D,%7B'option':'UTF8','string':'someinitialvalue'%7D,'CBC','Raw','Raw',%7B'option':'Hex','string':''%7D,%7B'option':'Hex','string':''%7D)