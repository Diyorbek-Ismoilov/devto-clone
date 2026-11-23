from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "blogapp"

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("post/<slug:slug>/", views.post_detail, name="post_detail"),
    path("post/<slug:slug>/edit/", views.post_edit, name="post_edit"),
    path("post/<slug:slug>/delete/", views.post_delete, name="post_delete"),
    path("tag/<slug:slug>/", views.tag_posts, name="tag_posts"),
    path("write/", views.post_create, name="post_create"),
    path("register/", views.register, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="blogapp/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]