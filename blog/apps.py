import os
import joblib
from django.apps import AppConfig
from django.conf import settings


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'


class ApiConfig(AppConfig):
    name = 'api'
    MODEL_FILE = os.path.join(settings.MODELS, "MultinomialNaiveBayesModel.joblib")
    model = joblib.load(MODEL_FILE)


class VectorizerConfig(AppConfig):
    name = 'api2'
    MODEL_FILE = os.path.join(settings.MODELS, "MultinomialNaiveBayesModelVectorizer.pickle")
    model = joblib.load(MODEL_FILE)
