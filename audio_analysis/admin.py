from django.contrib import admin
from .models import AudioFile, SentimentAnalysis

admin.site.register(AudioFile)
admin.site.register(SentimentAnalysis)
