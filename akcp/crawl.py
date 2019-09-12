from bs4 import BeautifulSoup as bs
import requests as req 
import re
import time
def get_soup(link):
    response = req.get(link)
    return bs(response.text, "html5lib")

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

def format_spec_list(lis):
    return re.sub("\s+", " ", re.sub("\n+", "**", lis))
def is_spec(a):
    return a.get_text().strip().lower().startswith("specification")

def get_spec_tab(soup):
    try:
        return next(filter(is_spec, soup.select(".x-nav-tabs-item a")))["href"]
    except:
        return None
     
def get_first_spec(soup):
    if not get_table(soup):
        return dict()
    soup = soup.find("div", {"id":get_table(soup)[1:]})
    if not soup:
        return "N/A"
    tds = soup.find_all("td")
    specs = dict()
    i = 0
    while i < len(tds):
        if tds[i].strong:
            if not tds[i].strong.next_sibling:
                i+=1
                continue
            if not tds[i].strong.next_sibling.next_sibling:
                i+=1
                continue
            if tds[i].strong.next_sibling.next_sibling.name:
                    if tds[i].strong.next_sibling.next_sibling.name=="td":
                        # print("Here 1")
                        specs[tds[i].strong.get_text()] = format_spec_list(tds[i+1].get_text())
                        i+=2
                        continue
            if tds[i].strong.next_sibling.next_sibling.next_sibling.name == "ul":
                # print("Here 2")
                string = join_list(tags_to_strings(tds[i].strong.next_sibling.next_sibling.next_sibling.find_all("li")))
                specs[tds[i].strong.string] =  string
                i+=1
                continue
            if tds[i].strong.next_sibling.next_sibling.next_sibling.name == "p":
                # print("Here 3")
                ps = tds[i].strong.next_sibling.next_sibling.next_siblings
                ps = "".join([p.get_text().replace("\n", "**") for p in ps])
                specs[tds[i].strong.get_text()] = ps
                i+=1
                continue
        
        if tds[i].b:
            if not tds[i].next_sibling :
                i+=2
                continue
            if not tds[i].next_sibling.next_sibling:
                i+=2
                continue
            if tds[i].next_sibling.next_sibling.name == "td":
                # print("Here 4")
                specs[tds[i].b.get_text()] = format_spec_list(tds[i+1].get_text())
                i+=2
            i+=2
            continue
        # print("Here 7")
        i+=1
        print(i)
    return specs

            

def tags_to_strings(tags):
    return map(lambda tag: re.sub("\s+", " ",tag.get_text()), tags)
def join_list(lis):
    return remove_all_spaces("**".join(lis))
def get_table(soup):
    return get_spec_tab(soup)


links = open("f.txt", "r")
listing = open("listing.csv", "a+")
begin = 16
for link in links.readlines()[begin:]:
    print(link)
    soup = get_soup(link.strip())
    soup = get_important(soup)
    name = soup.find("span", {"class": "entry-title"}).get_text()
    image = get_image(soup)
    try:
        desc = get_desc(soup)
    except:
        desc = "N/A"
    # try :
    #     spec = get_first_spec(soup)
    # except:
    #     spec = dict()
    specs = "N/A"
    # if len(spec)>0:
    #     for key, value in spec.items():
    #         specs += key+"\t"+value
    listing.write(
        ";".join(
            (name,
            desc,
            specs,
            image)
        )+"\n"
    )
    print("pausing")
    time.sleep(10)
    