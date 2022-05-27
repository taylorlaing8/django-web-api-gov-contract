from django.urls import include, path
from . import views

urlpatterns = [
    path(
        "user/",
        include(
            [
                path("create/", views.UserCreate.as_view()),
                path("", views.UserList.as_view()),
                path("<int:pk>/", views.UserDetail.as_view()),
                path("update/<int:pk>/", views.UserUpdate.as_view()),
                path("delete/<int:pk>/", views.UserDelete.as_view()),
            ]
        ),
    )
]
