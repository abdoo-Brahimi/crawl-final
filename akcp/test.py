import requests as req
from bs4 import BeautifulSoup as bs

def get_soup(link):
    response = req.get(link)
    return bs(response.text, features="html5lib")

link = "https://www.akcp.com/products/sensorprobe-plus/spx-plus/"

soup = get_soup(link)
main = soup.find("article",["page", "type-page", "status-publish", "hentry", "no-post-thumbnail"])
bands = main.select(".x-content-band.vc")


