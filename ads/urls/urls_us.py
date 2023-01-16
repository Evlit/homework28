from django.urls import path

from ads.views import views_us

urlpatterns = [
    path("", views_us.UserListView.as_view()),
    path("<int:pk>/", views_us.UserDetailView.as_view()),
    path("create/", views_us.UserCreateView.as_view()),
    path("<int:pk>/update/", views_us.UserUpdateView.as_view()),
    path("<int:pk>/delete/", views_us.UserDeleteView.as_view()),
]
