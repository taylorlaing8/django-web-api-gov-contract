from django.urls import include, path
from .views import *

urlpatterns = [
    path(
        "contract/",
        include(
            [
                path(
                    "positions/",
                    include(
                        [
                            path("create/", PositionCreate.as_view()),
                            path("", PositionList.as_view()),
                            path("<int:pk>/", PositionDetail.as_view()),
                            path("<int:pk>/update/", PositionUpdate.as_view()),
                            path("<int:pk>/delete/", PositionDelete.as_view()),
                        ]
                    ),
                ),
                path(
                    "pocs/",
                    include(
                        [
                            path("create/", PointOfContactCreate.as_view()),
                            path("", PointOfContactList.as_view()),
                            path("<int:pk>/", PointOfContactDetail.as_view()),
                            path("<int:pk>/update/", PointOfContactUpdate.as_view()),
                            path("<int:pk>/delete/", PointOfContactDelete.as_view()),
                        ]
                    ),
                ),
                path(
                    "contracts/",
                    include(
                        [
                            path("create/", ContractCreate.as_view()),
                            path("", ContractList.as_view()),
                            path("<int:pk>/", ContractDetail.as_view()),
                            path("<int:pk>/update/", ContractUpdate.as_view()),
                            path("<int:pk>/delete/", ContractDelete.as_view()),
                        ]
                    ),
                ),
                path(
                    "tasks/",
                    include(
                        [
                            path("create/", TaskCreate.as_view()),
                            path("", TaskList.as_view()),
                            path("<int:pk>/", TaskDetail.as_view()),
                            path("<int:pk>/update/", TaskUpdate.as_view()),
                            path("<int:pk>/delete/", TaskDelete.as_view()),
                        ]
                    ),
                )
            ]
        ),
    )
]
