import requests as req
from bs4 import BeautifulSoup as bs

def get_soup(link):
    response = req.get(link)
    return bs(response.text, features="html5lib")

link = "https://www.akcp.com/products/sensorprobe-plus/spx-plus/"

soup = get_soup(link)
main = soup.find("article",["page", "type-page", "status-publish", "hentry", "no-post-thumbnail"])
bands = main.select(".x-content-band.vc")

bands = [band for band in bands if band.get_text(strip=True)!=""]
bands = bands[:-1]
print(len(bands))
# bands = bands[1:-1] if bands[0].find("script") else bands[:-1]
# print(len(bands))
# print(len(main.find_all("div", recursive=False)))

# print(main.find(["h2", "h1"]))

# https://www.akcp.com/products/racks-din-accessories/demo-kits/
# https://www.akcp.com/modbus-gateway/
# https://www.akcp.com/rack-plus/rfid-swing-handle-lock/