from PIL import Image, ImageDraw, ImageFont
from random import choice, randint
import os
import requests

persons = ['ibuki', 'nagito', 'soda']
person = choice(persons)

path_background = "backgrounds/"
path_person = f"{person}/"

image_background_filename = choice([
  x for x in os.listdir(path_background)
  if os.path.isfile(os.path.join(path_background, x))
])

image_person_filename = choice([
  x for x in os.listdir(path_person)
  if os.path.isfile(os.path.join(path_person, x))
])

def prepare_text(text=None):
    brk = []
    for i in range(1, 7):
        brk.append(60*i)
    i = 0
    splited = text.split()
    new_text = ''
    for part in splited:
        if len(new_text + part) < brk[i]:
            new_text += part +' '
        else:
            new_text += '\n' +part +' '
            i += 1
    return new_text

def getData():
  response = requests.get('https://www.boredapi.com/api/activity/')
  res = response.json()
  return res

def create_image():
  text = 'Put some plants and put them around your house'
  img_background = Image.open(f"backgrounds/{image_background_filename}")
  img_person = Image.open(f"{person}/{image_person_filename}")
  img_template = Image.open(f"template1.png")
  
  mask_im = Image.new("RGBA", img_background.size, 0)
  MASK_IMG = Image.open(f"{person}/{image_person_filename}").convert('RGBA')
  mask_im.paste(img_background)
  size = int(img_background.width / 2)
  mask_im.paste(img_person, (size, 0), MASK_IMG)
  img_template_new = img_template.resize(img_background.size)
  mask_im.paste(img_template_new, (0,0), img_template_new)

  imgDraw = ImageDraw.Draw(mask_im)
  imgFont = ImageFont.truetype('fontdialogue.ttf', 30)
  txt = prepare_text(text)
  imgDraw.text((82, 428), txt, font=imgFont, fill=(255,255,255), spacing=0)
  chapter = randint(1, 5)
  imgFont1 = ImageFont.truetype('fontdialogue.ttf', 18)
  imgDraw.text((827, 13), f'0{chapter}', font=imgFont1, fill=(255,0,0), spacing=0)
  level = randint(10, 50)
  imgDraw.text((825, 52), f'{level}', font=imgFont1  , fill=(255,255,255), spacing=0)
  mask_im.save('test.png', quality=95)

  print(f'{image_person_filename} - {image_background_filename}')

if __name__ == "__main__":
  create_image()