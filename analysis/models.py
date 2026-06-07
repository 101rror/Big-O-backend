from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class AnalysisRecord(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="analysis_records"
    )
    code = models.TextField()
    language = models.CharField(max_length=64)
    ai_response = models.JSONField(blank=True, null=True)
    time_complexity = models.CharField(max_length=128)
    space_complexity = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "analysis"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.language} @ {self.created_at.isoformat()}"
