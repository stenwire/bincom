from django.urls import path

from . import views

urlpatterns = [
    path(
        "results/<int:pk>/",
        views.DisplayPollingUnitResult.as_view(),
        name="results",
    ),
    path("total/", views.DisplayTotalPollingUnitResult, name="total"),
    path("create/", views.StorePollingUnitResult, name="create"),
]
