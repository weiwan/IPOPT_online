from mongonaut.sites import MongoAdmin

# Import your custom models
from .models import *
from mongoengine.django.auth import User

User.mongoadmin = MongoAdmin()
Submission.mongoadmin = MongoAdmin()
Result.mongoadmin = MongoAdmin()
NLPModel.mongoadmin = MongoAdmin()
