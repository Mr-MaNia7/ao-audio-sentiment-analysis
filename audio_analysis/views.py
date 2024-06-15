from django.forms import ValidationError
import tensorflow as tf
import numpy as np
from audio_analysis.models import AudioAnalysis, Sentiment
from audio_analysis.utils.preprocessing import extract_features
from .serializers import AudioAnalysisSerializer
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
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
        
        if not file:
            raise ValidationError("No file provided")
        
        # Save the file temporarily
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file.read())
            temp_file_path = temp_file.name
            
        try:
            original_features = extract_features(temp_file_path)     
            all_features = np.array(original_features)
            input_data = np.expand_dims(all_features, axis=0)
            
            # Make a prediction
            prediction = model.predict(input_data)
            sentiment = np.argmax(prediction, axis=1)[0]
            
            # Map the sentiment to a label
            sentiment_label = self.map_sentiment_to_label(sentiment)
            confidence_score = prediction[0][sentiment] * 100
            
            audio_file = serializer.save(
                sentiment=sentiment_label,
                confidence_score=confidence_score      
            )
        except Exception as e:
            print(e)
        
        finally:
            os.remove(temp_file_path)

    def map_sentiment_to_label(self, sentiment):
        sentiment_map = {
            0: Sentiment.NEGATIVE,
            1: Sentiment.NEUTRAL,
            2: Sentiment.POSITIVE
        }
        return sentiment_map.get(sentiment, Sentiment.NEUTRAL).value
