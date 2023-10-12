import requests 
import sys

url = "http://" + sys.argv[1] + ":" + sys.argv[2] + "/AltoroJ"

s = requests.Session()

jSessionId = s.get(url, verify=0).cookies.get("JSESSIONID")
headers = {
    "Host": "localhost:8080",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux aarch64; rv:109.0) Gecko/20100101 Firefox/118.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "http://localhost:8080/AltoroJ/login.jsp",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "http://localhost:8080",
    "Connection": "keep-alive",
    "Cookie": "JSESSIONID="+str(jSessionId),
    "Upgrade-Insecure-Requests": "1",
}

data = "uid=%27+OR+1%3D1+--&passw=1234&btnSubmit=Login"

response = s.post(url+"/doLogin", headers=headers, data=data, allow_redirects=False)

if response.status_code == 302 and response.cookies.get("AltoroAccounts"):
    sys.exit(1)
else:
    sys.exit(0)
