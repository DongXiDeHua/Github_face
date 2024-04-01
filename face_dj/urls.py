"""
URL configuration for face_dj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from UI import views

urlpatterns = [
    # path("admin/", admin.site.urls),
    path("", views.index1),

    path("index/", views.index),

    path("root/", views.root),

    path("register/", views.register),

    path("root/index/", views.root_index),

    path("index/user_index/", views.user_index),

    path("root/root_index/user_manage/", views.user_manage),

    path("root/root_index/reptile_manage/", views.reptile_manage),

    path("root/root_index/face_manage/", views.face_manage),

    path("root/root_index/sum_manage/", views.sum_manage),

    path("root/root_index/user_manage/delete/", views.user_delete),

    path("index/user_index/reptile_view/", views.reptile_view),

    path("index/user_index/reptile_view_post/", views.reptile_view_post),

    path("index/user_index/reptile/", views.reptile),

    path("index/user_index/face/", views.face),

    path("index/user_index/face_view/", views.face_view),

    path("index/uer_index/face_view_post/", views.face_view_post),

    path("index/user_index/reptile/rootbilibili/", views.rootbilibili),

    path("index/user_index/reptile/userbilibili/", views.userbilibili),

    path("index/user_index/reptile/QQspace/", views.QQspace),

    path("index/user_index/reptile/rootxiaohongshu/", views.rootxiaohongshu),

    path("index/user_index/reptile/userxiaohongshu/", views.userbilibili),

    path("index/user_index/reptile/rootbilibili/rootbilibili_T/", views.rootbilibili_T),

    path("index/user_index/change_password/", views.change_password),

    path("index/user_cookie_delete/", views.user_cookie_delete),

    path("root/root_cookie_delete/", views.root_cookie_delete)

]
