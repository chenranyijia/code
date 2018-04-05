# -*- coding: utf-8 -*-
import os
os.chdir('C:\Users\chenran\Desktop')
import PIL.Image, PIL.ImageFont, PIL.ImageDraw
font = PIL.ImageFont.truetype('simsun.ttc',60)
im = PIL.Image.open('86836.jpg')
draw = PIL.ImageDraw.Draw(im)
text = unicode('02_02区域','utf-8')
draw.text((520,964), text, font=font, fill=(255,255,255))
text = unicode('02_03区域','utf-8')
draw.text((1036,964), text, font=font, fill=(255,255,255))
text = unicode('02_04区域','utf-8')
draw.text((1546,964), text, font=font, fill=(255,255,255))
im.save('chen.jpg')
