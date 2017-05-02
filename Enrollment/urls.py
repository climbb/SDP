from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    
    url(r'^mycourses/',views.mycourses),
    url(r'^view_users/$',views.view_users),
    url(r'^view_users/u/(?P<pk>[0-9]+)/$',views.view_user_completed),
    url(r'^course/(?P<pk>[0-9]+)/$', views.course_detail),
    url(r'^course/new/$', views.course_new, name='course_new'),
    url(r'^add/(?P<pk>[0-9]+)/',views.add),
    url(r'^enroll/$', views.enroll, name='view'),
    url(r'^enroll/course/(?P<pk>[0-9]+)/$', views.enroll_course_detail),
    url(r'^$', views.index),
    url(r'^managecourses/',views.managecourses),
    url(r'^createnewcourse/',views.course_new),
    url(r'^course_modules/(?P<pk>[0-9]+)/$', views.course_modules),
    url(r'^course_modules/(?P<pk>[0-9]+)/drop/$', views.course_drop),
    url(r'^course_modules/(?P<pk1>[0-9]+)/module(?P<pk2>[0-9]+)/$', views.course_module_detail),
    url(r'^course_modules/(?P<pk1>[0-9]+)/module(?P<pk2>[0-9]+)/c/(?P<pk3>[0-9]+)', views.course_component_detail),
    url(r'^edit_course/(?P<pk>[0-9]+)/$', views.edit_course),
    url(r'^edit_course/(?P<pk>[0-9]+)/edit_preferences/$', views.edit_course_preferences),
    url(r'^edit_course/(?P<pk1>[0-9]+)/moveup_module/m/(?P<pk2>[0-9]+)/$',views.moveup_module),
    url(r'^edit_course/(?P<pk1>[0-9]+)/movedown_module/m/(?P<pk2>[0-9]+)/$',views.movedown_module),
    url(r'^edit_course/(?P<pk1>[0-9]+)/add_new_module/$',views.module_new),
    url(r'^edit_course/(?P<pk1>[0-9]+)/delete_module/module(?P<pk2>[0-9]+)/$',views.module_delete),
    url(r'^edit_course/(?P<pk1>[0-9]+)/edit_components/module(?P<pk2>[0-9]+)/$',views.module_components),
    url(r'^edit_course/(?P<pk1>[0-9]+)/edit_components/module(?P<pk2>[0-9]+)/add_text/$',views.component_add_text),
    url(r'^edit_course/(?P<pk1>[0-9]+)/edit_components/module(?P<pk2>[0-9]+)/add_image/$',views.component_add_image),
    url(r'^edit_course/(?P<pk1>[0-9]+)/edit_components/module(?P<pk2>[0-9]+)/add_video/$',views.component_add_video),
    url(r'^edit_course/(?P<pk1>[0-9]+)/edit_components/module(?P<pk2>[0-9]+)/add_file/$',views.component_add_file),
    url(r'^edit_course/(?P<pk1>[0-9]+)/edit_components/module(?P<pk2>[0-9]+)/edit_TXT/c/(?P<pk3>[0-9]+)/$',views.component_edit_text),
    url(r'^edit_course/(?P<pk1>[0-9]+)/edit_components/module(?P<pk2>[0-9]+)/edit_IMG/c/(?P<pk3>[0-9]+)/$',views.component_edit_image),
    url(r'^edit_course/(?P<pk1>[0-9]+)/edit_components/module(?P<pk2>[0-9]+)/edit_VID/c/(?P<pk3>[0-9]+)/$',views.component_edit_video),
    url(r'^edit_course/(?P<pk1>[0-9]+)/edit_components/module(?P<pk2>[0-9]+)/edit_FIL/c/(?P<pk3>[0-9]+)/$',views.component_edit_file),
    url(r'^edit_course/(?P<pk1>[0-9]+)/edit_components/module(?P<pk2>[0-9]+)/delete_component/c/(?P<pk3>[0-9]+)/$',views.delete_component),
    url(r'^edit_course/(?P<pk1>[0-9]+)/edit_module/module(?P<pk2>[0-9]+)/$',views.edit_module),
    url(r'^edit_course/(?P<pk1>[0-9]+)/edit_components/module(?P<pk2>[0-9]+)/moveup_component/c/(?P<pk3>[0-9]+)/$',views.moveup_component),
    url(r'^edit_course/(?P<pk1>[0-9]+)/edit_components/module(?P<pk2>[0-9]+)/movedown_component/c/(?P<pk3>[0-9]+)/$',views.movedown_component),
    url(r'^edit_course/(?P<pk1>[0-9]+)/edit_components/module(?P<pk2>[0-9]+)/c/(?P<pk3>[0-9]+)/$',views.course_component_detail_instructor),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)