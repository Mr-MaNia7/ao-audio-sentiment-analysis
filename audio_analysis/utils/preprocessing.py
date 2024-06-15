import tensorflow as tf
import librosa
import numpy as np
import keras as K
import tensorflow as tf


def log_spectogram(audio, sample_rate, window_size, step_size, eps=1e-10):
    n_fft = int(window_size * sample_rate)
    hop_length = int(step_size * sample_rate)
    D = np.abs(librosa.stft(audio, n_fft=n_fft, hop_length=hop_length))
    D = np.log(D + eps)
    return D


def extract_features(file_path):
    X, sample_rate = librosa.load(file_path, duration=3, sr=22050*2, offset=0.5)
    return extract_features_helper(X, sample_rate=sample_rate)

def extract_features_helper(data, sample_rate):
    sample_rate = np.array(sample_rate)
    mfccs = np.mean(librosa.feature.mfcc(y=data, sr=sample_rate, n_mfcc=13), axis=0)
    if len(mfccs) < 259:
        mfccs = np.pad(mfccs, (0, 259 - len(mfccs)), mode='constant')
    elif len(mfccs) > 259:
        mfccs = mfccs[:259]

    return mfccs


def noise(data):
    if data.size == 0:
        return data
    noise_amp = 0.005 * np.random.uniform() * np.amax(data)
    data = data.astype('float64') + noise_amp * np.random.normal(size=data.shape[0])
    return data

def shift(data):
    if data.size == 0:
        return data
    s_range = int(np.random.uniform(low=-5, high=5) * 500)
    return np.roll(data, s_range)

def stretch(data, rate=0.8):
    if data.size == 0:
        return data
    data = librosa.effects.time_stretch(data, rate=rate)
    return data

def pitch(data, sample_rate):
    if data.size == 0:
        return data
    bins_per_octave = 12
    pitch_pm = 2
    pitch_change = pitch_pm * 2 * (np.random.uniform())
    data = librosa.effects.pitch_shift(y=data.astype('float64'), sr=sample_rate, n_steps=pitch_change, bins_per_octave=bins_per_octave)
    return data

def dyn_change(data):
    if data.size == 0:
        return data
    dyn_change = np.random.uniform(low=1.5, high=3)
    return data * dyn_change

def speedNpitch(data):
    if data.size == 0:
        return data
    length_change = np.random.uniform(low=0.8, high=1)
    speed_fac = 1.0 / length_change
    tmp = np.interp(np.arange(0, len(data), speed_fac), np.arange(0, len(data)), data)
    minlen = min(data.shape[0], tmp.shape[0])
    data *= 0
    data[0:minlen] = tmp[0:minlen]
    return data



def precision(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision



def recall(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall


def fscore(y_true, y_pred):
    if K.sum(K.round(K.clip(y_true, 0, 1))) == 0:
        return float(0)

    p = precision(y_true, y_pred)
    r = recall(y_true, y_pred)
    f_score = 2 * (p * r) / (p + r + K.epsilon())
    return f_score

def get_lr_metric(optimizer):
    def lr(y_true, y_pred):
        return optimizer.lr
    return lr
