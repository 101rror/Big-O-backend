from rest_framework import serializers
from .models import AnalysisRecord

LANGUAGE_CHOICES = [
    ("c", "C"),
    ("cpp", "C++"),
    ("python", "Python"),
    ("java", "Java"),
    ("javascript", "JavaScript"),
]


class AnalysisInputSerializer(serializers.Serializer):
    code = serializers.CharField()
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES)


class AnalysisOutputSerializer(serializers.Serializer):
    timeComplexity = serializers.CharField()
    spaceComplexity = serializers.CharField()
    explanation = serializers.DictField()
    suggestions = serializers.ListField(child=serializers.CharField())
    confidence = serializers.FloatField()


class AnalysisRecordSerializer(serializers.ModelSerializer):
    analysis = AnalysisOutputSerializer(source="ai_response")

    class Meta:
        model = AnalysisRecord
        fields = ["id", "code", "language", "created_at", "analysis"]
