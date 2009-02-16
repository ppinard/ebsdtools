import rmlimage.macro.python.gui

def within(im, x, y):
  if x >= 0 and x <= im.width and \
     y >= 0 and y <= im.height:
    return True
  else:
    return False

def flood_fill(im, x, y, value):
  "Flood fill on a region of non-BORDER_COLOR pixels."
  BORDER_COLOR = 0
  
  if not within(im, x, y) or im.getPixValue(x, y) == BORDER_COLOR:
    return
  
  edge = [(x, y)]
  im.setPixValue(x, y, value)
  
  while edge:
    newedge = []
    for (x, y) in edge:
      for (s, t) in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
        if within(im, s, t) and \
          im.getPixValue(s, t) not in (BORDER_COLOR, value):
            im.setPixValue(s, t, value)
            newedge.append((s, t))
    edge = newedge
  
if __name__ == '__main__':
  
  map = kernel.ByteMap(9, 9)
   
#  map.setFile('seedfill.bmp')
#  IO.save(map)
  
#  for x in range(9):
#    for y in range(9):
#      flood_fill(map, x, y, 128)  
  
