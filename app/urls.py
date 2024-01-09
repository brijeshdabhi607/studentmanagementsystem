from django.urls import path
from .import views

urlpatterns = [
    path("", views.home, name="home"),
    path("base/", views.base , name="base"),
    path("courses", views.single_course, name="courses"),
    path("contact/", views.contact, name="contact"),
    path("about/", views.about, name="about"),
    path("accounts/register/", views.register, name="register"),
    path("do_login/", views.do_login, name="do_login"),
    path("accounts/profile/", views.profile, name="profile"),
    path("accounts/profile/update/", views.update_profile, name="update_profile"),
    path("filter-data/", views.filter_data, name="filter-data"),
    path("search-course/", views.search_course, name="search_course"),
]