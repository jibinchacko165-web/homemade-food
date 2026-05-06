from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Extended User model supporting customers and chefs"""
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('chef', 'Chef'),
        ('admin', 'Administrator'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    is_seller = models.BooleanField(default=False)  # Keep for backward compatibility
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_chef(self):
        return self.role == 'chef' or self.is_seller
    
    @property
    def is_admin_user(self):
        return self.role == 'admin' or self.is_superuser
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
