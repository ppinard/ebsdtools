
import RandomUtilities.sort.sortDict as sortDict
import EBSDTools.mathTools.vectors as vectors

orders = []
#orders.append({'indices': [0,0,0], 's': 0})

for i in range(-5, 5):
  for j in range(-5, 5):
    for k in range(-5, 5):
      square = i**2 + j**2 + k**2
      indices = [i, j, k]
      indices.sort()
      v = vectors.vector(indices)
      
      inOrders = False
      for order in orders:
        if order['s'] == square and (order['v'] == v or order['v'] == -v):
          inOrders = True
          break
          
      
      if inOrders == False:
        orders.append({'v': v, 's': square})
      

sortDict.sortListByKey(orders, 's')

for order in orders:
  print '%i %s' % (order['s'], order['v'])

#print orders