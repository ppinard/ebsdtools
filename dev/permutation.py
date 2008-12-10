
def permutation(mh, mk, ml):
  numpossible = 24
  
  p = {}
  
  p.setdefault(0, {})
  p[0][0] = mh
  p[0][1] = mk
  p[0][2] = ml
  iN = 0
  
  for l in range(6):
    if l < 3:
      i=l; j=(i+1)%3; k=(i+2)%3; ll=1
    else:
      j=l-3; i=(j+1)%3; k=(i+2)%3; ll=-1
    
    for ii in range(1,-3,-2):
      for jj in range(1,-3,-2):
        for kk in range(1,-3,-2):
          if ii*jj*kk < 0:
            continue
          
          iN += 1
          if iN >= numpossible: 
            return numpossible, p
          
          p.setdefault(iN, {})
          p[iN][0] = ii*p[0][i]
          p[iN][1] = jj*p[0][j]
          p[iN][2] = kk*p[0][k]
          
          for m in range(iN):
            if (p[m][0] == p[iN][0] and p[m][1] == p[iN][1] and p[m][2] == p[iN][2]) or \
              (p[m][0] == -p[iN][0] and p[m][1] == -p[iN][1] and p[m][2] == -p[iN][2]):
              iN -= 1
              break
  
  return iN + 1, p

if __name__ == '__main__':
  n, p = permutation(2,0,0)
  
  print n
  
  for perms in p:
    print '%2i%2i%2i' % (p[perms][0],p[perms][1],p[perms][2])