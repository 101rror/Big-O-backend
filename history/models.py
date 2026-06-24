from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class HistoryEntry(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="history_entries"
    )
    code = models.TextField()
    language = models.CharField(max_length=64)
    ai_response = models.JSONField()
    time_complexity = models.CharField(max_length=128)
    space_complexity = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"History entry for {self.user.username} at {self.created_at.isoformat()}"
        )
