
import json
from pathlib import Path


def rebuildItemModels():
  mcpath = Path()/'assets/minecraft'
  blockstats = mcpath/'blockstates'
  itemmodels = mcpath/'models/item'
  itemmodels.mkdir(parents=True,exist_ok=True)
  
  for file in blockstats.iterdir():
    if file.suffix == ".json":
      obj = json.loads(file.read_text())
      itempath = itemmodels/file.name
      if itempath.exists():
        # print(f'itemmodel for {file.stem} is already exists.')
        continue
      if 'variants' in obj:
        for case in ['','type=bottom','axis=x','facing=east,half=bottom,shape=straight']:
          if case in obj['variants']:
            itemmodel:str = obj['variants'][case]['model']
            itempath.write_text(f'{{"parent": "{itemmodel}"}}')
            break
        else:
          print(f'{file.stem} is unknown variant model.')
      else:
        print(f'{file.stem} is not variant model.')

rebuildItemModels()