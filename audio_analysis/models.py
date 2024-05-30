from django.db import models
from accounts.models import CustomUser as User

class AudioFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='audio_files/')
    upload_time = models.DateTimeField(auto_now_add=True)
    
    def get_file_url(self):
        return self.file.url

class SentimentAnalysis(models.Model):
    audio_file = models.ForeignKey(AudioFile, on_delete=models.CASCADE)
    sentiment = models.CharField(max_length=255)
    confidence_score = models.FloatField()
    analysis_time = models.DateTimeField()
