import os
import time
import json
from django.views import generic
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.files import File
from django.views.decorators.csrf import csrf_exempt

from three_d.models import TDModel, ObjModel
from linshi_3D import settings
from three_d.tools import handle_uploaded_file, handle_zip_file
from three_d.td_tools import find_the_edge_length


def allow_all(response):
    """
    解决跨域的问题
    :param response:
    :return:
    """
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def home_page(request):
    return render(request, 'index.html')


def test_js(request, p_id):
    project = get_object_or_404(TDModel, pk=p_id)
    response = render(request, 'free_look.html', {'path': project.uploads.url, 'host': request.get_host()})
    return allow_all(response)


def test_obj(request, p_id):
    project = get_object_or_404(ObjModel, pk=p_id)
    content = {
        'obj_path': project.upload_obj.url,
        'pic_path': project.upload_pic.url,
        'host': request.get_host(),
        'res': find_the_edge_length(project.upload_obj.path)
    }
    response = render(request, 'free_look.html', content)
    return allow_all(response)


class TDModelIndexView(generic.ListView):
    model = TDModel
    template_name = "tdmodel_index.html"
    paginate_by = 10   # 一个页面显示的条目
    context_object_name = "tdmodel_list"


class ObjModelIndexView(generic.ListView):
    model = ObjModel
    template_name = "objmodel_index.html"
    paginate_by = 10   # 一个页面显示的条目
    context_object_name = "objmodel_list"


@csrf_exempt
def load_obj_zip(request):
    """
    上传zip 包含（obj, pic, mtl）
    :param request:
    :return:
    """
    if request.method == 'POST':
        l_file = request.FILES.get('obj_zip')
        time_stamp = str(time.time()).split('.')[0]
        if l_file:
            try:
                path = os.path.join(settings.BASE_DIR, 'media', 'zip', time_stamp + str(l_file))
                handle_uploaded_file(l_file, path)

                # 解压 zip
                export_path = os.path.join(settings.BASE_DIR, 'media', 'zip', 'obj')
                files_info = handle_zip_file(path, export_path)

                obj_model = ObjModel(name=request.POST.get('name') or time_stamp)

                prefix_name = str(l_file).split('.')[0]
                obj_model.upload_obj.save(prefix_name+'.obj', File(open(files_info['obj'], 'rb')), save=False)
                obj_model.upload_pic.save(prefix_name+'.pic', File(open(files_info['pic'], 'rb')), save=False)
                obj_model.upload_mtl.save(prefix_name+'.mtl', File(open(files_info['mtl'], 'rb')), save=False)
                obj_model.save()
                response = HttpResponse(
                    json.dumps({'state': 0, 'message': "OK ! New model's name : %s" % obj_model.name}),
                    content_type="application/json"
                )
            except Exception as e:
                print(e)
                response = HttpResponse(
                    json.dumps({'state': 100, 'message': 'has error during creating model'}),
                    content_type="application/json"
                )
        else:
            response = HttpResponse(json.dumps({'state': 200, 'message': 'without zip file'}),
                                    content_type="application/json")
        return allow_all(response)
    else:
        return render(request, 'uploads_zip.html')






