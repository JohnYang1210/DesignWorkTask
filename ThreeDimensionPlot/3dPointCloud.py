import numpy as np

def viz_mayavi(points, vals="height"):
    x = points[:, 0]  # x position of point
    y = points[:, 1]  # y position of point
    z = 2*points[:, 2]  # z position of point
    # r = lidar[:, 3]  # reflectance value of point
    d = np.sqrt(x ** 2 + y ** 2)  # Map Distance from sensor

    # Plot using mayavi -Much faster and smoother than matplotlib
    import mayavi.mlab

    if vals == "height":
        col = z
    else:
        col = d

    fig = mayavi.mlab.figure(bgcolor=(0, 0, 0), size=(640, 360))
    mayavi.mlab.points3d(x, y, z,
                         col,          # Values used for Color
                         mode="point",
                         colormap='spectral', # 'bone', 'copper', 'gnuplot'
                         # color=(0, 1, 0),   # Used a fixed (r,g,b) instead
                         figure=fig,
                         )
    mayavi.mlab.show()

points = np.loadtxt('3DPointCloudKuashan.txt',delimiter=',')
# filename=input('input file path and name')
# points=np.loadtxt(filename,delimiter=',')
viz_mayavi(points)
