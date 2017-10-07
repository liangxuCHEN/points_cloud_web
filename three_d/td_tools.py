from pyntcloud import PyntCloud
import pandas as pd
import numpy as np


K_TREE_NUM = 25
Z_MAX = 0.18
R = 0.035

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
    model  = PyntCloud.from_file(file_name)
    kdtree = model.add_structure("kdtree")
    # 外部区分
    voxelgrid = model.add_structure("voxelgrid", sizes=[0.05] * 3)
    clusters = model.add_scalar_field("euclidean_clusters", voxelgrid=voxelgrid)
    drop_cloud = PyntCloud(model.points[model.points[clusters]==0.0])
    # 平滑处理
    drop_cloud.points['sor'] = drop_cloud.get_filter("SOR", kdtree=kdtree, k=K_TREE_NUM, z_max=0.18)
    # 轮廓特征
    drop_cloud.points['ror'] = drop_cloud.get_filter("ROR", kdtree=kdtree, k=K_TREE_NUM, r=0.075)
    drop_cloud.points.drop(drop_cloud.points[(drop_cloud.points['sor']==False) | (drop_cloud.points['ror']==False)].index, inplace=True)
    
    # 内部区分
    drop_cloud = PyntCloud(drop_cloud.points)
    voxelgrid = drop_cloud.add_structure("voxelgrid", sizes=[0.03] * 3)
    clusters = drop_cloud.add_scalar_field("euclidean_clusters", voxelgrid=voxelgrid)
    gc = drop_cloud.points.groupby(clusters).size().sort_values(ascending=False)
    # 添加颜色
    drop_cloud.points['red']=pd.Series([0] * (x.points.index.max()+1))
    drop_cloud.points['green']=pd.Series([100] * (x.points.index.max()+1))
    drop_cloud.points['blue']=pd.Series([0] * (x.points.index.max()+1))

    red = pd.Series([0] * (x.points.index.max()+1))
    blue = pd.Series([0] * (x.points.index.max()+1))
    for i in gc[:5].index:
        for red_index in drop_cloud.points[drop_cloud.points[clusters]==i].index:
            red[red_index] = ((i + 10) * 3) % 255
            blue[red_index] = ((i + 2) * 2) % 255
        #print(x.points[x.points[clusters]==i]['blue'])
    drop_cloud.points['red'] =  red
    drop_cloud.points['blue'] =  blue

    # 保存处理后的版本
    x.points.drop(['ror', 'sor', clusters], 1, inplace=True)
    x.to_file('sample_'+file_name)