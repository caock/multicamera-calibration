import numpy as np
from scipy.spatial.transform import Rotation as R

r = R.from_rotvec([-11.488576787378843, -7.076667088675427, 23.796329235686507])
m = r.as_matrix()
v = np.array([0,0,1]).reshape(3, 1)
v2 = np.matmul(m, v)
print(v2.shape)
print(v2)