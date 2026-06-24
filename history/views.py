from rest_framework import generics, permissions
from .models import HistoryEntry
from .serializers import HistoryEntrySerializer


# Create your views here.
class HistoryListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HistoryEntrySerializer

    def get_queryset(self):
        return HistoryEntry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HistoryDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HistoryEntrySerializer
    lookup_field = "pk"

    def get_queryset(self):
        return HistoryEntry.objects.filter(user=self.request.user)
