from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('content=<int:pk>', views.content_view, name="content_view"),
    path('content_approval', views.content_approval, name="content_approval"),
    path('login', views.login_page, name="login"),
    path('logout', views.logout_user, name="logout"),
    path('notification', views.notification_view, name="notification"),
    path('settings', views.user_settings, name="settings"),
    path('edit_profile', views.edit_profile, name="edit_profile"),
    path('profile/<int:pk>', views.user_profile, name="profile"),
    path('change_profile_picture', views.change_profile_picture, name="change_profile_picture"),
]
