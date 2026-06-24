from rest_framework import serializers
from .models import HistoryEntry


class HistoryEntrySerializer(serializers.ModelSerializer):
    analysis = serializers.JSONField(write_only=True, required=False)
    ai_response = serializers.JSONField(required=False)
    time_complexity = serializers.CharField(required=False, allow_blank=True)
    space_complexity = serializers.CharField(required=False, allow_blank=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)

    class Meta:
        model = HistoryEntry
        fields = [
            "id",
            "code",
            "language",
            "analysis",
            "ai_response",
            "time_complexity",
            "space_complexity",
            "createdAt",
        ]
        read_only_fields = ["id", "createdAt"]

    def create(self, validated_data):
        analysis = validated_data.pop("analysis", {}) or {}
        validated_data["ai_response"] = {
            k: v
            for k, v in analysis.items()
            if k not in ["timeComplexity", "spaceComplexity"]
        }
        validated_data["time_complexity"] = analysis.get("timeComplexity", "")
        validated_data["space_complexity"] = analysis.get("spaceComplexity", "")
        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["analysis"] = {
            "timeComplexity": representation.pop("time_complexity"),
            "spaceComplexity": representation.pop("space_complexity"),
            **(instance.ai_response or {}),
        }
        return representation
