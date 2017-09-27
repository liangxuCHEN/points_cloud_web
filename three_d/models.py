from django.db import models

# Create your models here.
class TDModel(models.Model):
    name = models.CharField(u'模型名字', max_length=128)
    uploads = models.FileField(u'上传文件', upload_to='model/ply')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def __unicode__(self):
        return '%s' % self.name


class ObjModel(models.Model):
    name = models.CharField(u'模型名字', max_length=128)
    upload_obj = models.FileField(u'上传obj文件', upload_to='model/obj')
    upload_pic = models.FileField(u'上传pic文件', upload_to='model/obj')
    upload_mtl = models.FileField(u'上传mtl文件', upload_to='model/obj', null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def __unicode__(self):
        return '%s' % self.name

#
# class Obj_zip_Model(models.Model):
#     name = models.CharField(u'模型名字', max_length=128)
#     upload_obj = models.FileField(u'上传obj文件', upload_to='model/obj')
#     upload_pic = models.FileField(u'上传pic文件', upload_to='model/obj')
#     upload_mtl = models.FileField(u'上传mtl文件', upload_to='model/obj', null=True)
#     created = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         ordering = ('created',)
#
#     def __unicode__(self):
#         return '%s' % self.name
