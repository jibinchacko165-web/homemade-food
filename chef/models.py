from django.db import models
from django.conf import settings


class FoodItem(models.Model):
    CATEGORY_CHOICES = (
        ('Breakfast', 'Breakfast (6:00 AM - 12:00 PM)'),
        ('Lunch', 'Lunch (12:00 PM - 3:30 PM)'),
        ('Snacks', 'Snacks (3:30 PM - 6:30 PM)'),
        ('Dinner', 'Dinner (6:30 PM - 3:00 AM)'),
    )
    
    chef = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'chef'},
        related_name='food_items'
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Breakfast')
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='food_images/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True, help_text='Paste an external image URL (e.g. from Imgur or Google Drive)')
    is_available = models.BooleanField(default=True)
    preparation_time = models.PositiveIntegerField(default=30, help_text='Minutes')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0, help_text='Out of 5')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.chef.username}"
    
    class Meta:
        verbose_name = 'Food Item'
        verbose_name_plural = 'Food Items'
        ordering = ('-created_at',)


class ChefProfile(models.Model):
    chef = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chef_profile'
    )
    bio = models.TextField(blank=True)
    specialty = models.CharField(max_length=200, blank=True, help_text='e.g., Kerala Cuisine, North Indian, etc.')
    years_of_experience = models.PositiveIntegerField(default=0)
    total_orders = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.chef.username}'s Profile"
    
    class Meta:
        verbose_name = 'Chef Profile'
        verbose_name_plural = 'Chef Profiles'
