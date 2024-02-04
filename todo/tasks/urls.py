
from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('add_task', views.add_task, name='add_task'),
    path('delete_task/<int:task_id>', views.delete_task, name='delete_task'),
    path('edit_task/<int:task_id>', views.edit_task, name='edit_task'),
    path("login_view/", views.login_view, name="login_view"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]

