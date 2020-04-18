"Module to test the basta app models"
from django.test import TestCase
from django.contrib.auth.models import User
from unittest import mock
from .models import Categories, Play, Session

# Write your tests here

class TestBastaModels(TestCase):
    def setUp(self):
        self.cat = Categories.objects.create(
            machinename="testcategory",
            verbosename="Test Category",
            maxlength=10,
        )
        self.user = User.objects.create(
            username="testuser",
            password="testpass1",
        )

