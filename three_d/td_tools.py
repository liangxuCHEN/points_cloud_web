from pyntcloud import PyntCloud
import pandas as pd
from pyntcloud.structures import ConvexHull
from pyntcloud.structures import Delaunay3D
import numpy as np
import math

K_TREE_NUM = 25
Z_MAX = 0.18
R = 0.035
VOXEL_SIZE = 0.1


# Binning:
def binning(col):
    div_num = 10
    # Define min and max values:
    minval = col.min()
    maxval = col.max()
    per_length = (maxval - minval) / div_num
    cut_points = [minval + per_length * i for i in range(0, div_num + 1)]
    # create list by adding min and max to cut_points

    labels = range(len(cut_points) - 1)

    # Binning using cut function of pandas
    colBin = pd.cut(col, bins=cut_points, labels=labels, include_lowest=True)
    return colBin


def find_the_edge_length(file_name):
    # read the model
    obj_model = PyntCloud.from_file(file_name)
    # 区分6个平面
    obj_model.points['gz'] = binning(obj_model.points["z"])
    plant_z = pd.value_counts(obj_model.points['gz'], sort=True)
    obj_model.points['gx'] = binning(obj_model.points["x"])
    plant_x = pd.value_counts(obj_model.points['gx'], sort=True)
    obj_model.points['gy'] = binning(obj_model.points["y"])
    plant_y = pd.value_counts(obj_model.points['gy'], sort=True)

    # 区分max min
    # 分辨是max or min
    index_z = {'max': plant_z.index[0], 'min': plant_z.index[1]} if plant_z.index[0] > plant_z.index[1] else {
        'min': plant_z.index[0], 'max': plant_z.index[1]}
    index_y = {'max': plant_y.index[0], 'min': plant_y.index[1]} if plant_y.index[0] > plant_y.index[1] else {
        'min': plant_y.index[0], 'max': plant_y.index[1]}
    index_x = {'max': plant_x.index[0], 'min': plant_x.index[1]} if plant_x.index[0] > plant_x.index[1] else {
        'min': plant_x.index[0], 'max': plant_x.index[1]}

    # 结果
    result = {}
    # 4个高度
    pole_0 = obj_model.points[(obj_model.points['gz'] == index_z['max']) & (
        obj_model.points['gy'] == index_y['max']) & (obj_model.points['gx'] == index_x['min'])]['z']
    pole_1 = obj_model.points[(obj_model.points['gz'] == index_z['min']) & (
        obj_model.points['gy'] == index_y['max']) & (obj_model.points['gx'] == index_x['min'])]['z']
    result['face_left_height'] = pole_0.median() - pole_1.median()

    pole_0 = obj_model.points[(obj_model.points['gz'] == index_z['max']) & (
        obj_model.points['gy'] == index_y['max']) & (obj_model.points['gx'] == index_x['max'])]['z']
    pole_1 = obj_model.points[(obj_model.points['gz'] == index_z['min']) & (
        obj_model.points['gy'] == index_y['max']) & (obj_model.points['gx'] == index_x['max'])]['z']
    result['face_right_height'] = pole_0.median() - pole_1.median()

    pole_0 = obj_model.points[(obj_model.points['gz'] == index_z['max']) & (
        obj_model.points['gy'] == index_y['min']) & (obj_model.points['gx'] == index_x['max'])]['z']
    pole_1 = obj_model.points[(obj_model.points['gz'] == index_z['min']) & (
        obj_model.points['gy'] == index_y['min']) & (obj_model.points['gx'] == index_x['max'])]['z']
    result['back_right_height'] = pole_0.median() - pole_1.median()

    pole_0 = obj_model.points[(obj_model.points['gz'] == index_z['max']) & (
        obj_model.points['gy'] == index_y['min']) & (obj_model.points['gx'] == index_x['max'])]['z']
    pole_1 = obj_model.points[(obj_model.points['gz'] == index_z['min']) & (
        obj_model.points['gy'] == index_y['min']) & (obj_model.points['gx'] == index_x['max'])]['z']
    result['back_left_height'] = pole_0.median() - pole_1.median()

    # 4个水平长度
    pole_0 = obj_model.points[(obj_model.points['gz'] == index_z['min']) & (
        obj_model.points['gy'] == index_y['max']) & (obj_model.points['gx'] == index_x['max'])]['x']
    pole_1 = obj_model.points[(obj_model.points['gz'] == index_z['min']) & (
        obj_model.points['gy'] == index_y['max']) & (obj_model.points['gx'] == index_x['min'])]['x']
    result['face_bottom_length'] = pole_0.median() - pole_1.median()

    pole_0 = obj_model.points[(obj_model.points['gz'] == index_z['max']) & (
        obj_model.points['gy'] == index_y['max']) & (obj_model.points['gx'] == index_x['max'])]['x']
    pole_1 = obj_model.points[(obj_model.points['gz'] == index_z['max']) & (
        obj_model.points['gy'] == index_y['max']) & (obj_model.points['gx'] == index_x['min'])]['x']
    result['face_above_length'] = pole_0.median() - pole_1.median()

    pole_0 = obj_model.points[(obj_model.points['gz'] == index_z['min']) & (
        obj_model.points['gy'] == index_y['min']) & (obj_model.points['gx'] == index_x['max'])]['x']
    pole_1 = obj_model.points[(obj_model.points['gz'] == index_z['min']) & (
        obj_model.points['gy'] == index_y['min']) & (obj_model.points['gx'] == index_x['min'])]['x']
    result['back_bottom_length'] = pole_0.median() - pole_1.median()

    pole_0 = obj_model.points[(obj_model.points['gz'] == index_z['max']) & (
        obj_model.points['gy'] == index_y['min']) & (obj_model.points['gx'] == index_x['max'])]['x']
    pole_1 = obj_model.points[(obj_model.points['gz'] == index_z['max']) & (
        obj_model.points['gy'] == index_y['min']) & (obj_model.points['gx'] == index_x['min'])]['x']
    result['back_above_length'] = pole_0.median() - pole_1.median()

    # 4个深度
    pole_0 = obj_model.points[(obj_model.points['gz'] == index_z['min']) & (
        obj_model.points['gy'] == index_y['max']) & (obj_model.points['gx'] == index_x['max'])]['y']
    pole_1 = obj_model.points[(obj_model.points['gz'] == index_z['min']) & (
        obj_model.points['gy'] == index_y['min']) & (obj_model.points['gx'] == index_x['max'])]['y']
    result['face_right_bottom'] = pole_0.median() - pole_1.median()

    pole_0 = obj_model.points[(obj_model.points['gz'] == index_z['max']) & (
        obj_model.points['gy'] == index_y['max']) & (obj_model.points['gx'] == index_x['max'])]['y']
    pole_1 = obj_model.points[(obj_model.points['gz'] == index_z['max']) & (
        obj_model.points['gy'] == index_y['min']) & (obj_model.points['gx'] == index_x['max'])]['y']
    result['face_right_above'] = pole_0.median() - pole_1.median()

    pole_0 = obj_model.points[(obj_model.points['gz'] == index_z['min']) & (
        obj_model.points['gy'] == index_y['max']) & (obj_model.points['gx'] == index_x['min'])]['y']
    pole_1 = obj_model.points[(obj_model.points['gz'] == index_z['min']) & (
        obj_model.points['gy'] == index_y['min']) & (obj_model.points['gx'] == index_x['min'])]['y']
    result['face_left_bottom'] = pole_0.median() - pole_1.median()

    pole_0 = obj_model.points[(obj_model.points['gz'] == index_z['max']) & (
        obj_model.points['gy'] == index_y['max']) & (obj_model.points['gx'] == index_x['min'])]['y']
    pole_1 = obj_model.points[(obj_model.points['gz'] == index_z['max']) & (
        obj_model.points['gy'] == index_y['min']) & (obj_model.points['gx'] == index_x['min'])]['y']
    result['face_left_above'] = pole_0.median() - pole_1.median()

    return result


def filter_points(file_name):
    model = PyntCloud.from_file(file_name)

    # 外部区分
    voxelgrid = model.add_structure("voxelgrid", sizes=[0.05] * 3)
    clusters = model.add_scalar_field("euclidean_clusters", voxelgrid=voxelgrid)
    drop_cloud = PyntCloud(model.points[model.points[clusters] == 0.0])

    # 内部区分

    voxelgrid = drop_cloud.add_structure("voxelgrid", sizes=[0.03] * 3)
    clusters = drop_cloud.add_scalar_field("euclidean_clusters", voxelgrid=voxelgrid)
    gc = drop_cloud.points.groupby(clusters).size().sort_values(ascending=False)
    # 添加颜色
    drop_cloud.points['red'] = pd.Series([0] * (drop_cloud.points.index.max() + 1))
    drop_cloud.points['green'] = pd.Series([100] * (drop_cloud.points.index.max() + 1))
    drop_cloud.points['blue'] = pd.Series([0] * (drop_cloud.points.index.max() + 1))

    red = pd.Series([0] * (drop_cloud.points.index.max() + 1))
    blue = pd.Series([0] * (drop_cloud.points.index.max() + 1))
    for i in gc[:5].index:
        for red_index in drop_cloud.points[drop_cloud.points[clusters] == i].index:
            red[red_index] = ((i + 10) * 3) % 255
            blue[red_index] = ((i + 2) * 2) % 255
            # print(x.points[x.points[clusters]==i]['blue'])
    drop_cloud.points['red'] = red
    drop_cloud.points['blue'] = blue

    # 保存处理后的版本
    drop_cloud.points.drop(['ror', 'sor', clusters], 1, inplace=True)
    drop_cloud.to_file('sample_' + file_name)


def chose_voxelgrid(cloud):
    vg_id = cloud.add_structure("voxelgrid", sizes=[VOXEL_SIZE] * 3)
    sample = cloud.get_sample("voxelgrid_centers", voxelgrid=vg_id)
    return PyntCloud(sample)


def outlet(cloud):
    kdtree = cloud.add_structure("kdtree")
    # 平滑处理
    cloud.points['sor'] = cloud.get_filter("SOR", kdtree=kdtree, k=K_TREE_NUM, z_max=0.18)
    # 轮廓特征
    cloud.points['ror'] = cloud.get_filter("ROR", kdtree=kdtree, k=K_TREE_NUM, r=0.075)
    cloud.points.drop(
        cloud.points[(cloud.points['sor'] == False) | (cloud.points['ror'] == False)].index,
        inplace=True)
    return PyntCloud(cloud.points)


def filter_outer_points(cloud):
    voxelgrid = cloud.add_structure("voxelgrid", sizes=[0.05] * 3)
    clusters = cloud.add_scalar_field("euclidean_clusters", voxelgrid=voxelgrid)
    return PyntCloud(cloud.points[cloud.points[clusters] == 0.0])


def find_plane(filename):
    origin_cloud = PyntCloud.from_file(filename)
    cloud = filter_outer_points(origin_cloud)
    cloud = outlet(cloud)
    cloud = chose_voxelgrid(cloud)
    k_neighbors = cloud.get_neighbors(k=25)
    ev = cloud.add_scalar_field('eigen_values', k_neighbors=k_neighbors)
    plan_fit = cloud.add_scalar_field('planarity', ev=ev)

    cloud = add_rgb(cloud, key=plan_fit)


def add_rgb(cloud, key=None):
    cloud.points['green'] = pd.Series([0] * (cloud.points.index.max() + 1))
    cloud.points['blue'] = pd.Series([255] * (cloud.points.index.max() + 1))
    if key:
        red = pd.Series([0] * (cloud.points.index.max() + 1))
        for i in cloud.points.index:
            if cloud.points.loc[i][key] > 0.7:
                red[i] = 255
        cloud.points['red'] = red
    else:
        cloud.points['red'] = pd.Series([0] * (cloud.points.index.max() + 1))
    return cloud

def find_top_points(cloud):
    """
        +++ : 0
        ++- : 1
        +-+ : 2
        +-- : 3
        -++ : 4
        -+- : 5
        --+ : 6
        --- : 7
    """
    # 添加一列距离信息
    cloud.points = cloud.points.apply(distance_from_centre, args=(cloud.centroid,), axis=1)
    p_index = cloud.points.sort_values('distence', ascending=False).index
    p_dict = generate_dict

    green = pd.Series([0] * (cloud.points.index.max() + 1))
    cloud.points['red'] = pd.Series([0] * (cloud.points.index.max() + 1))
    cloud.points['blue'] = pd.Series([125] * (cloud.points.index.max() + 1))

    for i in cloud.points.index:
        if i in p_index:
            code = ''
            if cloud.points.loc[i]['x'] >= cloud.centroid[0]:
                code += '1'
            else:
                code += '0'
            if cloud.points.loc[i]['y'] >= cloud.centroid[1]:
                code += '1'
            else:
                code += '0'
            if cloud.points.loc[i]['z'] >= cloud.centroid[2]:
                code += '1'
            else:
                code += '0'
            if p_dict[code] < 0:
                p_dict[code] = i
                green[i] = 255

    cloud.points['green'] = green


def distance_from_centre(row, p):
    # 计算 点到中心点的距离
    data = row[['x', 'y', 'z']]
    row['distence'] = math.sqrt((data['x'] - p[0]) ** 2 + (data['y'] - p[1]) ** 2 + (data['z'] - p[2]) ** 2)
    return row


# 记录各象限
def generate_dict():
    points_index = dict()
    for x in range(8):
        value = bin(x)[2:]
        num_zero = 3 - len(value)
        if num_zero == 1:
            value = '0' + value
        if num_zero == 2:
            value = '00' + value

        points_index[value] = -1
    return points_index


# 曲率找边框
def find_edg_by_curvature(cloud):
    k_neighbors = cloud.get_neighbors(k=60)
    ev = cloud.add_scalar_field('eigen_values', k_neighbors=k_neighbors)
    line_fit = cloud.add_scalar_field("curvature", ev=ev)

    add_rgb(cloud, key=line_fit)


# get mesh 添加面
def get_mesh(cloud):
    # furthest_site 连接最远点
    # ConvexHull 凸包，外围点
    # process = ConvexHul(cloud)
    process = Delaunay3D(cloud, furthest_site=True)
    process.extract_info()
    process.compute()
    cloud.mesh = process.get_mesh()
    return cloud