from rest_framework import serializers
from .models import AudioAnalysis
import magic

def validate_audio_file(file):
    mime = magic.Magic(mime=True)
    file_mime_type = mime.from_buffer(file.read(2048))  # Read the first few bytes of the file
    file.seek(0)  # Reset file pointer after reading
    print("file_mime_type", file_mime_type)

    if not (file_mime_type.startswith('audio/') or file_mime_type.startswith('video/webm')):
        raise serializers.ValidationError("Invalid file type. Only audio files are allowed.")

class AudioAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioAnalysis
        fields = '__all__'

    file = serializers.FileField(validators=[validate_audio_file])

    file_url = serializers.SerializerMethodField()

    def get_file_url(self, obj):
        return obj.get_file_url()
