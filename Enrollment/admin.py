from django.contrib import admin
from embed_video.admin import AdminVideoMixin

# Register your models here.

from .models import Category
from .models import Course
from .models import Instructor
from .models import Participant
from .models import Enrollment
from .models import Module
from .models import Component




from django.contrib.auth import models as auth_models
from functools import partial

#admin.site.register(Course)
admin.site.register(Category)
admin.site.register(Instructor)
admin.site.register(Participant)
admin.site.register(Enrollment)
#admin.site.register(Module)

class ComponentAdmin(AdminVideoMixin, admin.ModelAdmin):
    pass
    
    list_display = ('module', 'name', 'instructor', 'component_type', 'text', 'image', 'file', 'video', 'file','position')
    list_filter = ('instructor',)
    exclude = ['instructor']

    def get_queryset(self, request):
        qs = super(ComponentAdmin, self).get_queryset(request)
        print ('hi world')
        if request.user.is_superuser:
            print ('hey')
            return qs
        else:
            print ('yo')
            return qs.filter(instructor=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'module':
            if not request.user.is_superuser:
                kwargs["queryset"] = Module.objects.filter(
                    instructor=request.user)
        return super(ComponentAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.instructor = request.user
        obj.save()

    def has_change_permission(self, request, obj=None):
        if not obj:
            return True # So they can see the change list page
        if request.user.is_superuser or obj.instructor == request.user:
            return True
        else:
            return False
    
    has_delete_permission = has_change_permission


admin.site.register(Component, ComponentAdmin)



class CourseAdmin(admin.ModelAdmin):
 
    

    def get_changeform_initial_data(self, request):
        return {'instructor': request.user}

    list_display = ('code', 'name', 'description', 'instructor', 'category')
    list_filter = ('instructor',)
    exclude = ['instructor']

    def get_queryset(self, request):
        qs = super(CourseAdmin, self).get_queryset(request)        
        if request.user.is_superuser:
            print ('hey')
            return qs
        else:
            print ('yo')
            return qs.filter(instructor=request.user)

    def save_model(self, request, obj, form, change):
        obj.instructor = request.user
        obj.save()

    def has_change_permission(self, request, obj=None):
        if not obj:
            return True # So they can see the change list page
        if request.user.is_superuser or obj.instructor == request.user:
            return True
        else:
            return False
    
    has_delete_permission = has_change_permission


admin.site.register(Course, CourseAdmin)

class ModuleAdmin(admin.ModelAdmin):
    
    list_display = ('course', 'name', 'visible', 'instructor', 'position')
    list_filter = ('instructor',)
    exclude = ['instructor']

    def get_queryset(self, request):
        qs = super(ModuleAdmin, self).get_queryset(request)
        print ('hi world')
        if request.user.is_superuser:
            print ('hey')
            return qs
        else:
            print ('yo')
            return qs.filter(instructor=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'course':
            if not request.user.is_superuser:
                kwargs["queryset"] = Course.objects.filter(
                    instructor=request.user)
        return super(ModuleAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.instructor = request.user
        obj.save()

    def has_change_permission(self, request, obj=None):
        if not obj:
            return True # So they can see the change list page
        if request.user.is_superuser or obj.instructor == request.user:
            return True
        else:
            return False
    
    has_delete_permission = has_change_permission

admin.site.register(Module, ModuleAdmin)