from audio_analysis.models import AudioFile
from .serializers import AudioFileSerializer
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import AudioFileSerializer

class AudioFileViewSet(viewsets.ModelViewSet):
    queryset = AudioFile.objects.all()
    serializer_class = AudioFileSerializer
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        audio_file = serializer.save()
