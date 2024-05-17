from django.contrib import admin
from .models import *
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from import_export.admin import ImportExportModelAdmin


class MyUserAdmin(BaseUserAdmin):
    list_display=('username', 'email', 'date_joined', 'last_login', 'is_admin', 'is_active')
    search_fields=('email','username', 'first_name', 'last_name')
    readonly_fields=('date_joined', 'last_login')
    filter_horizontal=()
    list_filter=('last_login',)
    fieldsets=()

    add_fieldsets=(
        (None,{
            'classes':('wide'),
            'fields':('email', 'username', 'first_name', 'middle_name', 'last_name', 'phone', 'password1', 'password2'),
        }),
    )

    ordering=('email',)

@admin.register(Students)
class StudentsAdmin(ImportExportModelAdmin):
    list_display = ['id' , 'StudentName','Class','StatusFee', 'StudentLocation', 'Gender', 'ParentNumber', 'created','last_updated']
    list_filter=['created','last_updated']
    search_fields = ["StudentName"]



class ClassesAdmin(admin.ModelAdmin):
    list_display = ['id', 'ClassName','ClassFee','SemisterFee','Created','Updated']
    list_filter=['Created','Updated']
    search_fields = ["ClassName"]

class SemisterAdmin(admin.ModelAdmin):
    list_display = ['SemisterName','SemisterFee','Created','Updated']
    list_filter=['Created','Updated']
    search_fields = ["SemisterName"]

class YearsAdmin(admin.ModelAdmin):
    list_display = ['id', 'Year','Created','Updated']
    list_filter=['Created','Updated']
    search_fields = ["Year"]

   
# admin.site.register(Students,StudentsAdmin)
admin.site.register(Classes,ClassesAdmin)
admin.site.register(Semister,SemisterAdmin)
admin.site.register(Years,YearsAdmin)

admin.site.register(MyUser, MyUserAdmin)

# admin.site.register(Courses)
# admin.site.register(Years)
