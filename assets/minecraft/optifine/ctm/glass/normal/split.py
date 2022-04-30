from pathlib import Path
from PIL import Image

dir = Path(__file__).parent
im = Image.open(dir/'all.png')

assert im.width % 5 == 0
unit = im.width // 5
assert im.height == unit

for x in range(5):
  im.crop((unit*x,0,unit*(x+1),unit)).save(dir/f'{x}.png')
