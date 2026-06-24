from django.urls import path
from .views import HistoryListCreateView, HistoryDeleteView

urlpatterns = [
    path("", HistoryListCreateView.as_view(), name="history_list_create"),
    path("<int:pk>/", HistoryDeleteView.as_view(), name="history_delete"),
]
