from mongonaut.sites import MongoAdmin

# Import your custom models
from .models import *
from mongoengine.django.auth import User

Profile.mongoadmin = MongoAdmin()
