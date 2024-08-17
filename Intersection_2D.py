import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from mpl_toolkits.mplot3d import Axes3D  # 用于3D绘图


# 定义已知数据点和对应的值
# 插值点，也可以改成读取csv的，如果要读取csv，参考demo_control_position_ff_mode.py里的做法import panads就行
# points和value的形式也可以为下列这种：
# points = np.array([[0, 0], [1, 1], [2, 2]])
# values = np.array([1, 2, 3])
points = np.random.rand(100, 2) * 4 - 2  # 100个随机点在[-2, 2]区间
values = np.sin(points[:, 0]) * np.cos(points[:, 1])  # 对应的函数值

# 定义插值网格
grid_x, grid_y = np.mgrid[-2:2:100j, -2:2:100j]  # 100x100的网格

# 执行 cubic 插值
# method也可以设置为linear
grid_z = griddata(points, values, (grid_x, grid_y), method='cubic')

#------- 可视化结果(optional)
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')  # 创建一个3D绘图的坐标轴

# 绘制曲面
surf = ax.plot_surface(grid_x, grid_y, grid_z, cmap='viridis',
                       linewidth=0, antialiased=False)

# 添加颜色条
fig.colorbar(surf, shrink=0.5, aspect=10)
# 设置标签和标题
ax.set_xlabel('X coordinate')
ax.set_ylabel('Y coordinate')
ax.set_zlabel('Interpolated values')
ax.set_title('3D Surface Plot of Cubic Interpolation')
plt.show()

