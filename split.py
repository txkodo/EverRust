from pathlib import Path
from PIL import Image

# ctmstr = '''
# ################### #####  # #  #   
# #+##+  +  +##+  +##+  +  +  +  +  + 
# ############# ## ## ## ## ##    ## #
# ############# ## ## ## #  ## ## ##  
# #+##+  +  +##+  +# +  +# +  +  +  + 
# # ##       ########### ## #  #   #  
# # ##       ## #####  ###      #    #
# #+##+  +  +##+  + #+  +  +  +  +  + 
# # ##       ##    ## ##    ##    ##  
# # ##       ##    #  ## #  ##  # #xxx
# #+##+  +  +# +  +# +  +# +  +  + xxx
# ################ ####  #      # #xxx
# '''[1:-1]

# l = ctmstr.split('\n')

# ctmstates:dict[int,dict[str,bool]] = {}

# i = 0
# for y in range(4):
#   for x in range(12):
#     if i == 47:
#       break
#     cell = [[ c == ' ' for c in l[y*3+i][x*3:x*3+3]] for i in range(3)]
#     ctmstates[i] = {
#       'ul' : cell[0][0],
#       'u' : cell[0][1],
#       'ur' : cell[0][2],
#       'l' : cell[1][0],
#       'r' : cell[1][2],
#       'dl' : cell[2][0],
#       'd' : cell[2][1],
#       'dr' : cell[2][2],
#     }
#     i += 1

# print(ctmstates)


ctm = {
  0: {'ul': False, 'u': False, 'ur': False, 'l': False, 'r': False, 'dl': False, 'd': False, 'dr': False},
  1: {'ul': False, 'u': False, 'ur': False, 'l': False, 'r': True, 'dl': False, 'd': False, 'dr': False},
  2: {'ul': False, 'u': False, 'ur': False, 'l': True, 'r': True, 'dl': False, 'd': False, 'dr': False},
  3: {'ul': False, 'u': False, 'ur': False, 'l': True, 'r': False, 'dl': False, 'd': False, 'dr': False},
  4: {'ul': False, 'u': False, 'ur': False, 'l': False, 'r': True, 'dl': False, 'd': True, 'dr': False},
  5: {'ul': False, 'u': False, 'ur': False, 'l': True, 'r': False, 'dl': False, 'd': True, 'dr': False},
  6: {'ul': False, 'u': True, 'ur': False, 'l': False, 'r': True, 'dl': False, 'd': True, 'dr': False},
  7: {'ul': False, 'u': False, 'ur': False, 'l': True, 'r': True, 'dl': False, 'd': True, 'dr': False},
  8: {'ul': False, 'u': True, 'ur': True, 'l': True, 'r': True, 'dl': False, 'd': True, 'dr': False},
  9: {'ul': False, 'u': True, 'ur': False, 'l': True, 'r': True, 'dl': False, 'd': True, 'dr': True},
  10: {'ul': True, 'u': True, 'ur': False, 'l': True, 'r': True, 'dl': True, 'd': True, 'dr': False},
  11: {'ul': True, 'u': True, 'ur': True, 'l': True, 'r': True, 'dl': False, 'd': True, 'dr': False},
  12: {'ul': False, 'u': False, 'ur': False, 'l': False, 'r': False, 'dl': False, 'd': True, 'dr': False},
  13: {'ul': False, 'u': False, 'ur': False, 'l': False, 'r': True, 'dl': False, 'd': True, 'dr': True},
  14: {'ul': False, 'u': False, 'ur': False, 'l': True, 'r': True, 'dl': True, 'd': True, 'dr': True},
  15: {'ul': False, 'u': False, 'ur': False, 'l': True, 'r': False, 'dl': True, 'd': True, 'dr': False},
  16: {'ul': False, 'u': True, 'ur': False, 'l': False, 'r': True, 'dl': False, 'd': False, 'dr': False},
  17: {'ul': False, 'u': True, 'ur': False, 'l': True, 'r': False, 'dl': False, 'd': False, 'dr': False},
  18: {'ul': False, 'u': True, 'ur': False, 'l': True, 'r': True, 'dl': False, 'd': False, 'dr': False},
  19: {'ul': False, 'u': True, 'ur': False, 'l': True, 'r': False, 'dl': False, 'd': True, 'dr': False},
  20: {'ul': True, 'u': True, 'ur': False, 'l': True, 'r': True, 'dl': False, 'd': True, 'dr': False},
  21: {'ul': False, 'u': True, 'ur': False, 'l': True, 'r': True, 'dl': True, 'd': True, 'dr': False},
  22: {'ul': False, 'u': True, 'ur': False, 'l': True, 'r': True, 'dl': True, 'd': True, 'dr': True},
  23: {'ul': False, 'u': True, 'ur': True, 'l': True, 'r': True, 'dl': False, 'd': True, 'dr': True},
  24: {'ul': False, 'u': True, 'ur': False, 'l': False, 'r': False, 'dl': False, 'd': True, 'dr': False},
  25: {'ul': False, 'u': True, 'ur': True, 'l': False, 'r': True, 'dl': False, 'd': True, 'dr': True},
  26: {'ul': True, 'u': True, 'ur': True, 'l': True, 'r': True, 'dl': True, 'd': True, 'dr': True},
  27: {'ul': True, 'u': True, 'ur': False, 'l': True, 'r': False, 'dl': True, 'd': True, 'dr': False},
  28: {'ul': False, 'u': True, 'ur': False, 'l': False, 'r': True, 'dl': False, 'd': True, 'dr': True},
  29: {'ul': False, 'u': False, 'ur': False, 'l': True, 'r': True, 'dl': True, 'd': True, 'dr': False},
  30: {'ul': False, 'u': True, 'ur': True, 'l': False, 'r': True, 'dl': False, 'd': True, 'dr': False},
  31: {'ul': False, 'u': False, 'ur': False, 'l': True, 'r': True, 'dl': False, 'd': True, 'dr': True},
  32: {'ul': True, 'u': True, 'ur': True, 'l': True, 'r': True, 'dl': True, 'd': True, 'dr': False},
  33: {'ul': True, 'u': True, 'ur': True, 'l': True, 'r': True, 'dl': False, 'd': True, 'dr': True},
  34: {'ul': False, 'u': True, 'ur': True, 'l': True, 'r': True, 'dl': True, 'd': True, 'dr': False},
  35: {'ul': True, 'u': True, 'ur': False, 'l': True, 'r': True, 'dl': False, 'd': True, 'dr': True},
  36: {'ul': False, 'u': True, 'ur': False, 'l': False, 'r': False, 'dl': False, 'd': False, 'dr': False},
  37: {'ul': False, 'u': True, 'ur': True, 'l': False, 'r': True, 'dl': False, 'd': False, 'dr': False},
  38: {'ul': True, 'u': True, 'ur': True, 'l': True, 'r': True, 'dl': False, 'd': False, 'dr': False},
  39: {'ul': True, 'u': True, 'ur': False, 'l': True, 'r': False, 'dl': False, 'd': False, 'dr': False},
  40: {'ul': False, 'u': True, 'ur': True, 'l': True, 'r': True, 'dl': False, 'd': False, 'dr': False},
  41: {'ul': True, 'u': True, 'ur': False, 'l': True, 'r': False, 'dl': False, 'd': True, 'dr': False},
  42: {'ul': True, 'u': True, 'ur': False, 'l': True, 'r': True, 'dl': False, 'd': False, 'dr': False},
  43: {'ul': False, 'u': True, 'ur': False, 'l': True, 'r': False, 'dl': True, 'd': True, 'dr': False},
  44: {'ul': True, 'u': True, 'ur': False, 'l': True, 'r': True, 'dl': True, 'd': True, 'dr': True},
  45: {'ul': False, 'u': True, 'ur': True, 'l': True, 'r': True, 'dl': True, 'd': True, 'dr': True},
  46: {'ul': False, 'u': True, 'ur': False, 'l': True, 'r': True, 'dl': False, 'd': True, 'dr': False}
}


def is_subdict(d0:dict[str,bool],d1:dict[str,bool]):
  for k,v in d1.items():
    if k not in d0 or d0[k] == v:
      return False
  return True

def construct(map:list[tuple[dict[str,bool],str]]):
  results:list[str] = []
  for _,m in ctm.items():
    for sub,v in map:
      if is_subdict(m,sub):
        results.append(v)
        break
    else:
      assert False
  return results

def genCtmProperty(tile:str,applymap:list[tuple[dict[str,bool],str]]):
  values = construct(applymap)
  return f'''
matchTiles={tile}
method=ctm
tiles={" ".join(values)}
'''

def saveCtmProperty(path:Path,tile:str,applymap:list[tuple[dict[str,bool],str]]):
  path.write_text(genCtmProperty(tile,applymap))

def saveProperty(path:Path,method:str,matchtiles:tuple[str],tiles:list[str]):
  path.write_text(f'''
matchTiles={" ".join(matchtiles)}
method={method}
tiles={" ".join(tiles)}
''')

def ctm_compact(path:str|Path,*matchtiles:str):
  path = Path(path)
  name = path.stem
  image = Image.open(path)
  unit = image.height
  assert image.width == unit * 5
  tiles:list[str] = []
  for i in range(5):
    new_name = f'{name}{i}'
    image.crop((unit*i,0,unit*(i+1),unit)).save(path.with_stem(new_name))
    tiles.append(new_name)
  
  saveProperty(path.with_suffix('.properties'),'ctm_compact',matchtiles,tiles)

ctm_compact(r'\assets\minecraft\optifine\ctm\iron_panel\plane.png','textures/block/iron_panel/plane.png')
