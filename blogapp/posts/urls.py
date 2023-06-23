from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.posts_list,name='list'),
    path('create',views.posts_create),
    path('<slug:slug>',views.posts_detail,name='detail'),
    path('<slug:slug>/edit',views.posts_update,name='update'),
    path('<slug:slug>/delete',views.posts_delete),
]