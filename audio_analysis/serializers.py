from rest_framework import serializers
from .models import AudioFile, SentimentAnalysis
import magic

def validate_audio_file(file):
    mime = magic.Magic(mime=True)
    file_mime_type = mime.from_buffer(file.read(2048))  # Read the first few bytes of the file
    file.seek(0)  # Reset file pointer after reading

    if not file_mime_type.startswith('audio/'):
        raise serializers.ValidationError("Invalid file type. Only audio files are allowed.")

class AudioFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioFile
        fields = '__all__'
    
    file = serializers.FileField(validators=[validate_audio_file])


class SentimentAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = SentimentAnalysis
        fields = '__all__'
