from django.db import models
from accounts.models import CustomUser as User

class AudioFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_url = models.URLField()
    upload_time = models.DateTimeField(auto_now_add=True)

class SentimentAnalysis(models.Model):
    audio_file = models.ForeignKey(AudioFile, on_delete=models.CASCADE)
    sentiment = models.CharField(max_length=255)
    confidence_score = models.FloatField()
    analysis_time = models.DateTimeField()
