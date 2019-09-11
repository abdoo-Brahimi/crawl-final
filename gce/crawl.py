from bs4 import BeautifulSoup as bs
import requests as req
import re
def get_soup(link):
    response = req.get(link)
    return bs(response.text)

def get_code(soup):
    code = soup.select_one("#product_reference span")
    return code.get_text() if code else "N/A"
def get_name(soup):
    name = soup.select_one("#pb-left-column h1")
    return name.get_text().replace("/","-") if name else "N/A"
def get_price(soup):
    price = soup.select_one("#our_price_display")
    return  price.get_text().replace(",", ".") if price else "N/A"
def get_desc(soup):
    desc = soup.select_one("#short_description_content")
    return desc.get_text().replace("\s+"," ") if desc else "N/A"

def get_spec(soup):
    spec = soup.select_one("#idTab1")
    if not spec:
        return "N/A"
    ps = spec.find_all("p")
    lis = spec.find_all("li")
    return format_ps(ps) + format_li(lis)

def get_image(soup):
    image = soup.select_one("#thumbs_list a")
    return  image["href"] if image else "N/A"
def format_ps(ps):
    if not ps:
        return ""
    return " ".join([re.sub("\s+"," ",p.get_text()) for p in ps])

def format_li(lis):
    if not lis:
        return ""
    return " ".join([re.sub("\s+"," ",li.get_text()) for li in lis])

def crawl_page(link):
    soup = get_soup(link)
    return (get_code(soup), 
            get_name(soup), 
            get_desc(soup), 
            get_spec(soup), 
            get_price(soup), 
            get_image(soup))

def crawl_site(file):
    urls = open(file, "r")
    products = []
    for url in urls:
        product = crawl_page(url.strip())
        products.append(product)
    return products

def create_csv(products, file):
    with open(file, "w") as listing:
        for product in products:
            listing.write(";".join(product)+"\n")

# link = "http://gce-electronics.com/en/din-web-relay-board-server/1483-lan-controller-web-relay-board-ipx800-v4.html"
# print(crawl_page(get_soup(link)))

products = crawl_site("poducts_urls.txt")
create_csv(products, "listing-gce.csv")