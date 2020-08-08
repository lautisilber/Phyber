import matplotlib.pyplot as plt

ax1 = plt.subplot(121, projection='3d')
ax1.scatter(5, 5, 5, marker='o')
ax1.scatter(3, 5, 5, marker='o')
ax1.scatter(3, 3, 5, marker='o')
ax1.scatter(5, 3, 5, marker='o')

ax1.set_xlabel('X Label')
ax1.set_ylabel('Y Label')
ax1.set_zlabel('Z Label')

plt.show()