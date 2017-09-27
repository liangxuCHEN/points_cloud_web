import zipfile


def handle_uploaded_file(file, path):
    with open(path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


def handle_zip_file(path, export_path):
    files_info = dict()
    f = zipfile.ZipFile(path, 'r')

    for file in f.namelist():
        new_path = f.extract(file, export_path)
        file_type = new_path.split('.')[1]
        if file_type == 'obj':
            files_info['obj'] = new_path
        if file_type == 'jpg':
            files_info['pic'] = new_path
        if file_type == 'mtl':
            files_info['mtl'] = new_path
    return files_info
