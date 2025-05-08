from datetime import date, timedelta

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from tasks.models import Task, Group
from users.models import Department, ROLE_CHOICES


