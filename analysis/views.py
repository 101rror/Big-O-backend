from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .serializers import AnalysisInputSerializer, AnalysisOutputSerializer
from .services import AnalysisService


# Create your views here.
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def analyze_code(request):
    serializer = AnalysisInputSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    code = serializer.validated_data["code"]
    language = serializer.validated_data["language"]

    try:
        result = AnalysisService.analyze(code, language)
    except Exception as exc:
        return Response(
            {"detail": str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    output_serializer = AnalysisOutputSerializer(data=result)
    output_serializer.is_valid(raise_exception=True)
    return Response(output_serializer.data)
