from django.contrib import admin
from three_d.models import TDModel, ObjModel
# Register your models here.


class TDModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'uploads')


class ObjModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'upload_pic')

admin.site.register(TDModel, TDModelAdmin)
admin.site.register(ObjModel, ObjModelAdmin)
