import os
import requests as req
import urllib
import shutil
from PIL import Image
import xlsxwriter
def get_download_image(url, name):
    
        # os.mkdir(os.path.join("Products", name))
        image = urllib.parse.urljoin("http://gce-electronics.com/", url)
        r = req.get(image, stream=True)
        if r.status_code == 200:
            with open(os.path.join("Products",name+".png"), 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)

# begin = 0
# for prod in open("listing-gce.csv").readlines()[begin:]:
#     get_download_image(prod.strip().split(";")[-1], prod.strip().split(";")[0].replace("/", "-"))



def insert_images():
    f = open("listing-gce.csv")
    size = 128, 128
    index = 1
    workbook = xlsxwriter.Workbook('images.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.set_default_row(size[0])
    for line in f:
        line = line.strip().split(";")
        code = line[0]
        name = line[1]
        desc = line[2]
        price = line[-2]
        im = Image.open(os.path.join("Products", code+".png"))
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(os.path.join("Products2",code+".png"), "png")
        
        worksheet.insert_image("E"+str(index), os.path.join("Products2", code+".png"))
        worksheet.write("A"+str(index), code)
        worksheet.write("B"+str(index), name)
        worksheet.write("C"+str(index), desc)
        worksheet.write("D"+str(index), price)
        index+=1
    workbook.close()


        
        
insert_images()