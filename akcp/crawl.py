from bs4 import BeautifulSoup as bs
import requests as req 
import re

def get_soup(link):
    response = req.get(link)
    return bs(response.text, "lxml")

def get_important(soup):
    return soup.find("div", {"role":"main"}).article

def get_name(soup):
    return soup.find("p").get_text()
def get_image(soup):
    return soup.find("img")["src"]
def get_code(soup):
    return format_code(soup.find("li").get_text())

def format_code(text):
    return re.sub("\s+","",text.split(":")[-1])
def get_desc(soup):
    return "1-"+get_first_desc(soup)+" 2- "+get_second_desc(soup)
def get_first_desc(soup):
    ps = soup.find("ul").previous_siblings
    ps = map(lambda tag: tag.string, ps)
    return remove_all_spaces(" ".join(list(ps)[-1::-1]))
def get_second_desc(soup):
    return remove_all_spaces(soup.find("div", {"id":"tab-1"}).get_text())
def remove_all_spaces(text):
    return re.sub("\s+", " ", text)

def is_spec(a):
    return a.get_text().strip().lower().startswith("specification")

def get_spec_tab(soup):
    return next(filter(is_spec, soup.select(".x-nav-tabs-item a")))["href"]
def get_first_spec(soup):
    pass
link = "https://www.akcp.com/products/intelligent-sensors/vibrationdetect-sensor/"
soup = get_soup(link)
soup = get_important(soup)
# for p in get_first_desc(soup):
#     print(p)

# ps = get_first_desc(soup)

print(get_name(soup))

print(get_code(soup))
print(get_desc(soup))
print(get_image(soup))