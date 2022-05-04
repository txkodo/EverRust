from pathlib import Path
from typing import Optional
from PIL import Image

_basepath = Path()/'assets/minecraft'

assert _basepath.exists()

def _saveProperty(path:Path,method:str,matchtiles:str|list[str],tiles:list[str],**kwarg:str|list[str]):
  def tryjoin(value:str|list[str]):
    return value if isinstance(value,str) else " ".join(value)
  
  result = {
    'matchTiles':matchtiles,
    'method':method,
    'tiles':tiles,
    **kwarg
  }

  path.write_text('\n'.join(f'{k}={tryjoin(v)}' for k,v in result.items()))

class _RandomizableImage:
  def __init__(self,savedir:Path,name:str,tiles:list[Image.Image|None]) -> None:
    self.savedir = savedir
    self._name = name
    self.tiles = tiles
  
  def export(self,weights:Optional[list[int]]=None):
    i = 0
    self.savedir.mkdir(parents=True,exist_ok=True)
    for x in self.tiles:
      if x is not None:
        x.save(self.savedir/(self._sub_name(0)+'.png'))
        i += 1
    if i > 1:
      p = (self.savedir/self._sub_name(0)).relative_to(_basepath)
      file = self.savedir/f'{self._name}.properties'
      tiles = [self._sub_name(j) for j in range(i)]
      if weights:
        _saveProperty(file,'random',str(p),tiles,weights=[str(w) for w in weights])
      else:
        _saveProperty(file,'random',str(p),tiles)
  
  def _sub_name(self,index:int):
    return f'{self._name}_{index}'

  
  @property
  def name(self):
    return self._sub_name(0)

def _splitImage(path:Path,count_x:int,count_y:int) -> list[list[_RandomizableImage]]:
  image = Image.open(path)
  assert image.width % count_x == 0
  unit = image.width // count_x
  assert image.height % (unit * count_y) == 0
  repeat = image.height // (unit * count_y)

  images:list[list[_RandomizableImage]] = []
  i = 0
  folder = path.parent/path.stem
  for y in range(count_y):
    images.append([])
    for x in range(count_x):
      tiles:list[None|Image.Image] = []
      for r in range(repeat):
        crop = image.crop((unit*x,unit*(r*count_y+y),unit*(x+1),unit*(r*count_y+y+1)))
        if crop.getextrema()[3] == (0,0): # type: ignore
          tiles.append(None)
        else:
          tiles.append(crop)
      images[-1].append(_RandomizableImage(folder,str(i),tiles))
      i += 1

  return images

def ctm(path:str|Path,matchtiles:str|list[str],**kwarg:str|list[str]):
  path = Path(path)
  images = _splitImage(path,12,4)
  i = 0
  tiles:list[str] = []
  for y in images:
    for x in y:
      if i != 47:
        tiles.append(x.name)
        x.export()
      i += 1
  _saveProperty(path.with_suffix('0.properties'),'ctm',matchtiles,tiles,**kwarg)

@staticmethod
def ctm_compact(path:str|Path,matchtiles:str|list[str],**kwarg:str|list[str]):
  path = Path(path)
  images = _splitImage(path,5,1)
  i = 0
  tiles:list[str] = []
  for y in images:
    for x in y:
      tiles.append(x.name)
      x.export()
      i += 1
  _saveProperty(path.parent/path.stem/'0.properties','ctm_compact',matchtiles,tiles,**kwarg)

def ctm_fixed():
  pass

@staticmethod
def horizontal(path:str|Path,matchtiles:str|list[str],**kwarg:str|list[str]):
  path = Path(path)
  images = _splitImage(path,4,1)
  i = 0
  tiles:list[str] = []
  for y in images:
    for x in y:
      tiles.append(x.name)
      x.export()
      i += 1
  _saveProperty(path.parent/path.stem/'0.properties','horizontal',matchtiles,tiles,**kwarg)

@staticmethod
def vertical(path:str|Path,matchtiles:str|list[str],**kwarg:str|list[str]):
  path = Path(path)
  images = _splitImage(path,4,1)
  i = 0
  tiles:list[str] = []
  for y in images:
    for x in y:
      tiles.append(x.name)
      x.export()
      i += 1
  _saveProperty(path.parent/path.stem/'0.properties','vertical',matchtiles,tiles,**kwarg)


vertical(
  r'assets\minecraft\optifine\ctm\vine\cross.png',
  ['textures/block/vine/cross'],
  connect='block'
  )