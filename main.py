from PIL import Image, ImageFont, ImageDraw, ImageOps


photo_dir = "/home/paran/Dropbox/a4calendarpdf/photos/camphoto_684387517.jpg"



PHOTO_SIZE = 1280
PHOTO_MARGIN = 200

page = Image.new('RGB',
                 (5950, 8420),   # A4 at 72dpi
                 (255, 255, 255))  # White

def place_photo_in_page(page_im, photo_dir, position=(5950 - PHOTO_SIZE - PHOTO_MARGIN, PHOTO_MARGIN), rotation_degrees=90):

    im = Image.open(photo_dir)
    im = im.rotate(rotation_degrees, expand=True)


    size = (PHOTO_SIZE, PHOTO_SIZE)

    im.thumbnail(size,Image.ANTIALIAS)
    page_im.paste(im, position)  # Not centered, top-left corner






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



def add_text(page, text, pos):

    f = ImageFont.load_default()
    txt=Image.new('L', (5000,500))
    d = ImageDraw.Draw(txt)
    d.text( pos, "Someplace Near Boulder",  font=f, fill=255)
    w=txt.rotate(17.5,  expand=1)

    page.paste( ImageOps.colorize(w, (0,0,0), (255,255,84)), (242,60),  w)


    # f = ImageFont.load_default()
    # txt=Image.new('L', (500,50))
    # d = ImageDraw.Draw(txt)
    # d.text( pos, text,  font=f, fill=255)
    # w=txt.rotate(90,  expand=1)

    # page.paste( ImageOps.colorize(w, (0,0,0), (255,255,84)), pos,  w)



def place_week_in_page(page, first_day):
    page.text((10,10), "Hello World", fill=(255,255,0), )


current_day = day(day_number=31, week_day=1, month=8, year=2020)

for i in range(3000):
    current_day.print_day()
    print(current_day.get_day_text())
    current_day.next_day()




place_photo_in_page(page, photo_dir)

add_text(page, "test text", (2000, 3000))


page.text((50, 50), "hey")

page.save("res.pdf", 'PDF', quality=100)
