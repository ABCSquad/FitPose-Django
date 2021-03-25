import numpy as np
import math
def angle(a,b,c):
    ba = a - b
    bc = c - b
    angle = math.atan2(bc[1], bc[0]) - math.atan2(ba[1], ba[0])
    if (angle < 0):
        angle += 2 * math.pi
    angle_in_deg = (angle*180)/math.pi
    return angle_in_deg
    

a1 = 0.6*100,0*100
b1 = 0*100,0*100
c1 = 0*100,0.6*100
print(a1,"",b1,"",c1)
a2,b2,c2 = np.array(list(c1)), np.array(list(b1)), np.array(list(a1))
print(angle(a2,b2,c2))