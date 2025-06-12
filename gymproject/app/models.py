from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

# Extended user model with roles
class User(AbstractUser):
    ROLE_CHOICES = (
        ('member', 'Member'),
        ('trainer', 'Trainer'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    phone = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

# Model for admission details (only members admitted)
class Admission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Admission: {self.user.username} - {self.plan_name}"

# Admin posts (announcement or workout info)
class AdminPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
