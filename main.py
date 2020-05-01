from PIL import Image, ImageFont, ImageDraw, ImageOps
import calendar


preference_name = "Tamara"

DAY_FONT = "fonts/times_seriff.tff"
photo_dir = "/home/paran/Dropbox/a4calendarpdf/photos/square.png"

print("Print with document viewer, both sides short edge (flip)")

PHOTO_SIZE = 1280
PHOTO_MARGIN = 200
N_OF_WEEKS = 51


if preference_name == "Tamara":
    START_Y_POS_MARGIN_COEF = 1.0
    DAY_FONT = "fonts/times_seriff.ttf"
    DAY_FONT_CEX = 0.6
    EXTRA_LINES_MARGIN = 0.05
elif preference_name == "Natale":
    START_Y_POS_MARGIN_COEF = 0.0
    DAY_FONT = "fonts/FantasticPete3.03.ttf"
    DAY_FONT_CEX = 1.0
    EXTRA_LINES_MARGIN = 0.1



pages = []
for i in range(N_OF_WEEKS+1):
    page = Image.new('RGB',
                 (8420, 5950),   # A4 at 72dpi
                 (255, 255, 255))  # White
    pages.append(page)

def place_photo_in_page(page_im, photo_dir, position=(8420 - PHOTO_SIZE - PHOTO_MARGIN, 5950 - PHOTO_MARGIN - PHOTO_SIZE), rotation_degrees=0):

    im = Image.open(photo_dir)
    if rotation_degrees != 0:
        im = im.rotate(rotation_degrees, expand=True)


    size = (PHOTO_SIZE, PHOTO_SIZE)

    im.thumbnail(size,Image.ANTIALIAS)
    page_im.paste(im, position)  # Not centered, top-left corner



def replace_month_to_euskara(text):    
    str_monthdays = [-1, "Urtarrila", "Otsaila", "Martxoa", "Apirila", "Maiatza", "Ekaina", "Uztaila", "Abuztua", "Iraila", "Urria", "Azaroa", "Abendua"]
    text = text.replace("January", str_monthdays[1])
    text = text.replace("February", str_monthdays[2])
    text = text.replace("March", str_monthdays[3])
    text = text.replace("April", str_monthdays[4])
    text = text.replace("May", str_monthdays[5])
    text = text.replace("June", str_monthdays[6])
    text = text.replace("July", str_monthdays[7])
    text = text.replace("August", str_monthdays[8])
    text = text.replace("September", str_monthdays[9])
    text = text.replace("October", str_monthdays[10])
    text = text.replace("November", str_monthdays[11])
    text = text.replace("December", str_monthdays[12])

    return text


class day:

    str_weekdays = [-1, "Astelehena", "Asteartea", "Asteazkena", "Osteguna", "Ostirala", "Zapatua", "Igandea"]
    str_monthdays = [-1, "Urtarrila", "Otsaila", "Martxoa", "Apirila", "Maiatza", "Ekaina", "Uztaila", "Abuztua", "Iraila", "Urria", "Azaroa", "Abendua"]

    def __init__(self, day_number, week_day, month, year):
        self.day_number = day_number
        self.week_day = week_day
        self.month = month
        self.year = year

    def next_day(self):
        day_month = [-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if self.is_leap_year():
            day_month[2] = 29
        if self.day_number == day_month[self.month]:
            self.month = ((self.month) % 12) + 1
            self.day_number = 1
            if self.month == 1:
                self.year += 1
        else:
            self.day_number += 1
        self.week_day = (self.week_day) % 7 + 1

    def is_leap_year(self):
        if (self.year % 4) == 0:  
            if (self.year % 100) == 0:  
                if (self.year % 400) == 0:  
                    return True  
                else:  
                    return False  
            else:  
                return True  
        else:  
            return False  
    
    def print_day(self):
        print(str(self.year) + "-" + str(self.month) + "-" + str(self.day_number) + ", " + self.str_weekdays[self.week_day])

    def get_day_text(self):
        return str(self.str_weekdays[self.week_day] + ", " + self.str_monthdays[self.month] + " " + str(self.day_number))



def add_text(page, text_string, pos, font = "fonts/MonospaceTypewriter.ttf", cex = 1.0):

    font = ImageFont.truetype(font, size=int(cex * 500), encoding="unic")
    draw = ImageDraw.Draw(page)
    draw.text(pos, text_string, (0, 0, 0), font=font)
    # 
    # 
    # d = ImageDraw.Draw(txt)
    # d.text( pos, text,  font=f, fill=255)
    # w=txt.rotate(90,  expand=1)

    # page.paste( ImageOps.colorize(w, (0,0,0), (255,255,84)), pos,  w)



def place_week_in_page(page, first_day):
    page.text((10,10), "Hello World", fill=(255,255,0), )




def write_lef_half_page(page, first_day):
    PAGE_DIMS=(8420, 5950)

    pos_y = PHOTO_MARGIN*START_Y_POS_MARGIN_COEF
    size_of_day = (PAGE_DIMS[1]- PHOTO_MARGIN*2)/4.5

    for i in range(4):
        add_text(page, first_day.get_day_text(), (PHOTO_MARGIN, pos_y), font=DAY_FONT, cex=DAY_FONT_CEX)
        pos_y += EXTRA_LINES_MARGIN * size_of_day
        for j in range(4):
            add_text(page, "__________________________", (PHOTO_MARGIN, pos_y + (j+2)*(size_of_day / 7)), cex=0.5, font="fonts/times_seriff.ttf")
        first_day.next_day()
        pos_y += size_of_day



def write_right_half_page(page, first_day):
    PAGE_DIMS=(8420, 5950)

    pos_x = PAGE_DIMS[0] / 2 + PHOTO_MARGIN*2
    pos_y = PHOTO_MARGIN*START_Y_POS_MARGIN_COEF
    size_of_day = (PAGE_DIMS[1]- PHOTO_MARGIN*2)/4.5

    for i in range(3):
        add_text(page, first_day.get_day_text(), (pos_x, pos_y), font=DAY_FONT, cex=DAY_FONT_CEX)
        pos_y += EXTRA_LINES_MARGIN * size_of_day
        for j in range(4):
            add_text(page, "__________________________", (pos_x, pos_y + (j+2)*(size_of_day / 7)), cex=0.5, font="fonts/times_seriff.ttf")
        first_day.next_day()
        pos_y += size_of_day
    
    add_text(page, replace_month_to_euskara(str(calendar.month(first_day.year, first_day.month))), (pos_x, pos_y + size_of_day / 2 - 400), cex=0.25)


current_day = day(day_number=31, week_day=1, month=8, year=2020)
for idx in range(N_OF_WEEKS):

    # Left side

    if idx == (N_OF_WEEKS+1) / 2:
        IS_BACK_PAGE = True
    elif idx < (N_OF_WEEKS+1) / 2:
        IS_BACK_PAGE = True
    else:
        IS_BACK_PAGE = False

    left_page_indexes = list(range(2,N_OF_WEEKS,2)) + [N_OF_WEEKS+1] + list(range(N_OF_WEEKS,2,-2))
    right_page_indexes = list(reversed(left_page_indexes))

    print(idx / N_OF_WEEKS)
    place_photo_in_page(pages[right_page_indexes[idx] - 1], photo_dir)
    write_lef_half_page(pages[left_page_indexes[idx] - 1], current_day)
    write_right_half_page(pages[right_page_indexes[idx] - 1], current_day)

for idx, page in enumerate(pages):
    page.save("pages_res/res_{}.pdf".format(idx + 10000), 'PDF', quality=20)

del pages

import gc
gc.collect()


import os
os.system("sleep 4")
os.system("qpdf --empty --pages pages_res/*.pdf -- out.pdf")
