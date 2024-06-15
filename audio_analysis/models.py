from django.db import models
from django.utils.translation import gettext_lazy as _

class Sentiment(models.TextChoices):
    POSITIVE = 'positive', _('Positive')
    NEGATIVE = 'negative', _('Negative')
    NEUTRAL = 'neutral', _('Neutral')

class AudioAnalysis(models.Model):
    user_id = models.CharField(max_length=255)  # Storing only user identifier from Next.js
    file = models.FileField(upload_to='audio_files/')
    sentiment = models.CharField(max_length=10, choices=Sentiment.choices, default=Sentiment.NEUTRAL)
    confidence_score = models.FloatField()
    upload_time = models.DateTimeField(auto_now_add=True)

    def get_file_url(self):
        return self.file.url
