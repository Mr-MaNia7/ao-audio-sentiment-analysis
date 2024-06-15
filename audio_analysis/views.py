import tensorflow as tf
import numpy as np
from audio_analysis.models import AudioAnalysis
from audio_analysis.utils.preprocessing import extract_features
from .serializers import AudioAnalysisSerializer
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
import os
from django.conf import settings
from tensorflow.keras.initializers import Orthogonal 
from tensorflow.keras.layers import GRU
import tempfile

class CustomGRU(GRU):
    def __init__(self, *args, **kwargs):
        kwargs.pop('time_major', None)
        kwargs.pop('implementation', None)
        super().__init__(*args, **kwargs)

initializer = Orthogonal(gain=1.0, seed=None)

custom_objects = {
    'Orthogonal': initializer,
    'GRU': CustomGRU
}

model_path = os.path.join(settings.BASE_DIR, 'audio_analysis/models', 'aug_noiseNshift_model.h5')
model = tf.keras.models.load_model(model_path, custom_objects=custom_objects)

class AudioAnalysisViewSet(viewsets.ModelViewSet):
    queryset = AudioAnalysis.objects.all()
    serializer_class = AudioAnalysisSerializer
    parser_classes = (MultiPartParser, FormParser)
    
    def perform_create(self, serializer):
        file = self.request.data.get('file')
        
        # Save the file temporarily
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file.read())
            temp_file_path = temp_file.name
            
        original_features = extract_features(temp_file_path)     
        all_features = np.array(original_features)
        input_data = np.expand_dims(all_features, axis=0)
        
        # Make a prediction
        prediction = model.predict(input_data)
        sentiment = np.argmax(prediction, axis=1)[0]
        
        # Map the sentiment to a label
        sentiment_label = self.map_sentiment_to_label(sentiment)
        audio_file.sentiment = sentiment_label
        audio_file.confidence_score = 90.0  # Placeholder value
        
        audio_file = serializer.save()

        return Response({'audio_file': serializer.data}, status=status.HTTP_201_CREATED)

    def map_sentiment_to_label(self, sentiment):
            sentiment_mapping = {
                0: 'negative',
                1: 'neutral',
                2: 'positive'
            }
            return sentiment_mapping.get(sentiment, 'unknown')
