import pcl
import pcl.pcl_visualization
import numpy as np

point_cloud = pcl.load_XYZI('point_cloud.pcd')
points = point_cloud.to_array()[:, :3]
points = points[points[:,2] < 200]
points = points[points[:,2] > -5]
points = points[points[:,1] > -2]
points = points[points[:,0] > -2]

point_cloud_temp = pcl.PointCloud()
point_cloud_temp.from_array(points)
pcl.save(point_cloud_temp, 'point_cloud_temp.ply', format='ply')
modified_point_cloud = pcl.load_XYZI('point_cloud_temp.ply')
visual = pcl.pcl_visualization.CloudViewing()

visual.ShowGrayCloud(modified_point_cloud, b'cloud')

flag = True
while flag:
    pass
end