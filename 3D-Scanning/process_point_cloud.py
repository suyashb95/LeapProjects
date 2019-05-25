import pcl
import pcl.pcl_visualization

point_cloud = pcl.load_XYZI('point_cloud.ply')
visual = pcl.pcl_visualization.CloudViewing()

visual.ShowGrayCloud(point_cloud, b'cloud')

flag = True
while flag:
    flag != visual.WasStopped()
end