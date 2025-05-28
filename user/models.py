from django.contrib.auth.models import AbstractUser
from django.db import models
import random

class CustomUser(AbstractUser):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    email_otp = models.CharField(max_length=6, blank=True, null=True)

    def generate_otp(self):
        self.email_otp = str(random.randint(100000, 999999))
        self.save()
    
    def verify_otp(self, otp):
        """Verify the OTP"""
        if self.email_otp == otp:
            self.is_email_verified = True
            self.email_otp = None  # Clear OTP after verification
            self.save()
            return True
        return False

    def __str__(self):
        return self.username
