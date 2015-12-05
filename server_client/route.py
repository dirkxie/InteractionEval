width = 20
length = 20
nomRight = 'right'
nomLeft = 'left'
nomUp = 'up'
nomDown = 'down'

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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
  

  if (nomDir == 'right'):
    if (x_prev > x_crnt):
      return 'backward'
    elif (x_prev < x_crnt):
      return 'forward'
    elif (y_prev > y_crnt):
      return 'right'
    elif (y_prev < y_crnt):
      return 'left' 
    else:
      return 'right'

  elif (nomDir == 'left'):
    if (x_prev > x_crnt):
      return 'forward'
    elif (x_prev < x_crnt):
      return 'backward'
    elif (y_prev > y_crnt):
      return 'left'
    elif (y_prev < y_crnt):
      return 'right'
    else:
      return 'left'

  elif (nomDir == 'up'):
    if (x_prev > x_crnt):
      return 'right'
    elif (x_prev < x_crnt):
      return 'left'
    elif (y_prev > y_crnt):
      return 'forward'
    elif (y_prev < y_crnt):
      return 'backward'
    else:
      return 'up'

  elif (nomDir == 'down'):
    if (x_prev > x_crnt):
      return 'left'
    elif (x_prev < x_crnt):
      return 'right'
    elif (y_prev > y_crnt):
      return 'backward'
    elif (y_prev < y_crnt):
      return 'forward'
    else:
      return 'down'

def navigate(x_prev, y_prev, z_prev, x_crnt, y_crnt, z_crnt, x_des, y_des, z_des, mapTemp):

  print bcolors.OKGREEN + '[PHASE 3] ' + bcolors.ENDC,
  print 'Previous coordinates:', bcolors.WARNING + str(x_prev), ',', str(y_prev) , ',', str(z_prev) + bcolors.ENDC
  
  print bcolors.OKGREEN + '[PHASE 3] ' + bcolors.ENDC,
  print 'Current coordinates:', bcolors.WARNING + str(x_crnt), ',', str(y_crnt), ',', str(z_crnt) + bcolors.ENDC
  
  print bcolors.OKGREEN + '[PHASE 3] ' + bcolors.ENDC,
  print 'Destination:', bcolors.WARNING + str(x_des), ',', str(y_des), ',', str(z_des) + bcolors.ENDC
  
  print bcolors.OKGREEN + '[PHASE 4] ' + bcolors.ENDC,
  print 'Calculating direction'
 
  print bcolors.OKGREEN + '[PHASE 4] ' + bcolors.ENDC,

  #destination reached
  if ((x_crnt == x_des) and (y_crnt == y_des) and (z_crnt == z_des)):
    print bcolors.FAIL + 'You are at the destination.\n' + bcolors.ENDC
  #go upstairs on map
  elif (z_crnt < z_des): #and (mapTemp[x_crnt][y_crnt+1] != '#'):
    print bcolors.FAIL + 'You should move upstairs' + bcolors.ENDC
  
  #go downstairs on map
  elif (z_crnt > z_des): #and (mapTemp[x_crnt][y_crnt+1] != '#'):    
    print bcolors.FAIL + 'You should move downstairs' + bcolors.ENDC

  #go down on map
  elif (y_crnt < y_des) and (mapTemp[x_crnt][y_crnt+1] != '#'):
    print bcolors.FAIL + 'You should move', actualDir(x_prev, y_prev, x_crnt, y_crnt, 'down') + bcolors.ENDC

  #turn left on map
  elif (x_crnt > x_des) and (mapTemp[x_crnt-1][y_crnt] != '#'):
    print bcolors.FAIL + 'You should move', actualDir(x_prev, y_prev, x_crnt, y_crnt, 'left') + bcolors.ENDC 

  #go up on map
  elif (y_crnt > y_des) and (mapTemp[x_crnt][y_crnt-1] != '#'):
    print bcolors.FAIL + 'You should move', actualDir(x_prev, y_prev, x_crnt, y_crnt, 'up') + bcolors.ENDC

  #turn right on map
  elif (x_crnt < x_des) and (mapTemp[x_crnt+1][y_crnt] != '#'):
    print bcolors.FAIL + 'You should move', actualDir(x_prev, y_prev, x_crnt, y_crnt, 'right') + bcolors.ENDC

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
