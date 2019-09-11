from bs4 import BeautifulSoup as bs
import requests as req
import time


def get_soup(link):
    response = req.get(link)
    return bs(response.text)


def get_important(soup):
    return soup.find("section", {"class":["listing", "products", "row", "list"]})

def get_name(soup):
    return soup.find("a", {"class":"card-title"}).get_text()

def get_code(soup):
    return soup.find("dd").get_text()

def get_price(soup):
    return "N/A" if soup.select(".text-nowrap.pricealttext") else soup.select_one(".theprice.text-nowrap").get_text().strip() 

def get_image(soup):
    return soup.find("img")["src"]

def get_desc_link(soup):
    return soup.find("a", {"class":"card-title"})["href"]

def get_desc(soup):
    section = soup.find("section", {"itemprop":"description"})
    return format_desc(section.find_all("p"))if section else "N/A"

def format_desc(ps):
   return " ".join([p.get_text().replace("\s+"," ") for p in ps])

def crawl_site(link):
    products = []
    soup = get_soup(link)
    # print(soup)
    soup = get_important(soup)
    # print(soup)
    for article in soup.find_all("article"):
        # time.sleep(2)
        desc_soup = get_soup(get_desc_link(article))
        products.append(tuple([get_code(article), get_name(article), get_desc(desc_soup), get_price(article), get_image(article)]))
    return products

def create_csv(products, file):
    with open(file, "w") as listing:
        for product in products:
            listing.write(";".join(product)+"\n")


products = crawl_site("https://www.generex-webshop.de/lng/en/product-overview/?count=157")
print(products)
create_csv(products, "listing-genrex.csv")
    

