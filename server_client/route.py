width = 20
length = 20

def mapGen(mapTemp):
  for i in xrange (1, length-1):
    mapTemp [1][i] = ' '
    mapTemp [width-2][i] = ' '
    mapTemp [width/2][i] = ' '
  
  for i in xrange (1, width-1):
    mapTemp [i][1] = ' '
    mapTemp [i][length-2] = ' '
    mapTemp [i][length/2] = ' '

def actualDir(x_prev, y_prev, x_crnt, y_crnt, nomDir):
  nomRight = 'right'
  nomLeft = 'left'
  nomUp = 'up'
  nomDown = 'down'

  if (nomDir == 'right'):
    if (x_prev > x_crnt):
      return 'backward'
    elif (x_prev < x_crnt):
      return 'forward'
    elif (y_prev > y_crnt):
      return 'right'
    elif (y_prev < y_crnt):
      return 'left' 

  elif (nomDir == 'left'):
    if (x_prev > x_crnt):
      return 'forward'
    elif (x_prev < x_crnt):
      return 'backward'
    elif (y_prev > y_crnt):
      return 'left'
    elif (y_prev < y_crnt):
      return 'right'

  elif (nomDir == 'up'):
    if (x_prev > x_crnt):
      return 'right'
    elif (x_prev < x_crnt):
      return 'left'
    elif (y_prev > y_crnt):
      return 'forward'
    elif (y_prev < y_crnt):
      return 'backward'

  elif (nomDir == 'down'):
    if (x_prev > x_crnt):
      return 'left'
    elif (x_prev < x_crnt):
      return 'right'
    elif (y_prev > y_crnt):
      return 'backward'
    elif (y_prev < y_crnt):
      return 'forward'


def navigate(x_prev, y_prev, x_crnt, y_crnt, x_des, y_des, mapTemp):

  #destination reached
  if ((x_crnt == x_des) and (y_crnt == y_des)):
    print 'You are at the destination.\n'
  
  #turn right on map
  elif (x_crnt < x_des and mapTemp[x_crnt+1][y_crnt] != '#'):
    print 'You should move', actualDir(x_prev, y_prev, x_crnt, y_crnt, nomRight)

  #turn left on map
  elif (x_crnt > x_des and mapTemp[x_crnt-1][y_crnt] != '#'):
    print 'You should move', actualDir(x_prev, y_prev, x_crnt, y_crnt, nomLeft) 

  #go up on map
  elif (y_crnt > y_des and mapTemp[x_crnt][y_crnt-1] != '#'):
    print 'You should move', actualDir(x_prev, y_prev, x_crnt, y_crnt, nomUp)

  #go down on map
  elif (y_crnt < y_des and mapTemp[x_crnt][y_crnt+1] != '#'):
    print 'You should move', actualDir(x_prev, y_prev, x_crnt, y_crnt, nomDown)

#def main():
#  mapTemp = [['#' for i in range (width)] for j in range(length)] 
#  mapGen(mapTemp)
#  print mapTemp
#  
#  x_des = 10
#  y_des = 1
#
#  x_crnt = 18
#  y_crnt = 10
#  
#  x_prev = 10
#  y_prev = 10
#  navigate(x_prev, y_prev, x_crnt, y_crnt, x_des, y_des, mapTemp)

#main()
