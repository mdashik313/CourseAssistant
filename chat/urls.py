from django.urls import path

from . import views

urlpatterns = [
    path('', views.chat_list, name='chat'),
    path('group=<int:pk>', views.group_chat, name='group_chat'),
    path('private=<int:pk>', views.private_chat, name='private_chat'),
]
