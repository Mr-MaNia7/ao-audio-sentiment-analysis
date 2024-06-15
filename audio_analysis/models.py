from django.db import models
from enum import Enum

class Sentiment(Enum):
    POSITIVE = 'positive'
    NEGATIVE = 'negative'
    NEUTRAL = 'neutral'

class AudioAnalysis(models.Model):
    user_id = models.CharField(max_length=255)  # Storing only user identifier from Next.js
    file = models.FileField(upload_to='audio_files/')
    upload_time = models.DateTimeField(auto_now_add=True)
    sentiment = models.CharField(max_length=255, choices=[(tag, tag.value) for tag in Sentiment])
    confidence_score = models.FloatField()
    analysis_time = models.DateTimeField(auto_now_add=True)

    def get_file_url(self):
        return self.file.url
