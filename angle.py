import numpy as np

a = np.array([6,0])
b = np.array([0,0])
c = np.array([-6,0])

ba = a - b
bc = c - b

cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
angle = np.arccos(cosine_angle)

print(np.degrees(angle))
