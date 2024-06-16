from rest_framework import serializers
from .models import AudioAnalysis
import magic

def validate_audio_file(file):
    mime = magic.Magic(mime=True)
    file_mime_type = mime.from_buffer(file.read(2048))  # Read the first few bytes of the file
    file.seek(0)  # Reset file pointer after reading

    if not (file_mime_type.startswith('audio/') or file_mime_type.startswith('video/webm')):
        raise serializers.ValidationError("Invalid file type. Only audio files are allowed.")

class AudioAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioAnalysis
        fields = '__all__'
        read_only_fields = ['sentiment', 'confidence_score', 'upload_time']


    file = serializers.FileField(validators=[validate_audio_file])

    file_url = serializers.SerializerMethodField()
