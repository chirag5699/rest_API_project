from django.db import models
from user.models import User
from django.utils import timezone
from django.core.validators import RegexValidator

def upload_to(instance, filename):
    filepath = f"business/logo/{filename}"
    return filepath

def photo_location(instance, filename):
    businessfoldername = f"{instance.business.id}"
    filepath = f"business/{businessfoldername}/photo/{filename}"
    return filepath

def video_location(instance, filename):
    businessfoldername = f"{instance.business.id}"
    filepath = f"business/{businessfoldername}/video/{filename}"
    return filepath

def offer_location(instance, filename):
    businessfoldername = f"{instance.business.id}"
    filepath = f"business/{businessfoldername}/offer/{filename}"
    return filepath

def show_location(instance, filename):
    businessfoldername = f"{instance.business.id}"
    filepath = f"business/{businessfoldername}/show/{filename}"
    return filepath

class Business(models.Model):
    name = models.CharField(max_length=150, null=False)
    description = models.CharField(max_length=200, null=True)
    URL = models.URLField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=20, validators=[RegexValidator(regex='^(\+?\d{1,3})?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$')])
    latitude = models.DecimalField(max_digits=8, decimal_places=6)
    longitude = models.DecimalField(max_digits=8, decimal_places=6)
    address = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    logo = models.ImageField(upload_to=upload_to, blank=True, null=True)
    users = models.ManyToManyField(User, related_name='businesses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"(BUSINESS){self.name},  {self.description}"
    

class BusinessPhoto(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, null=False)
    photo = models.ImageField(upload_to=photo_location, blank=True, null=True)
    description = models.CharField(max_length=200, null=True)
    start_date = models.DateField(auto_now_add=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self) -> str:
        return f"(BUSINESS-PHOTO){self.name},  {self.description}"
    
class BusinessVideo(models.Model): 
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    video = models.FileField(upload_to=video_location, blank=True, null=True)
    name = models.CharField(max_length=150, null=False)
    description = models.CharField(max_length=300, null=True)
    start_date =  models.DateField(auto_now_add=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    pass_count = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"(BUSINESS-VIDEO){self.name},  {self.description}"


class Businesspdf(models.Model):
    """A model representing a offer made by the business."""
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    pdf = models.ImageField(upload_to=offer_location, blank=True, null=True)
    name = models.CharField(max_length=150, null=False)
    description = models.CharField(max_length=300, null=True)
    start_date =  models.DateField(auto_now_add=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    
    def __str__(self) -> str:
        return f"(BUSINESS-OFFER){self.name},  {self.description}"


class BusinessShow(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    show = models.FileField(upload_to=show_location, blank=True, null=True)
    name = models.CharField(max_length=150, null=False)
    description = models.CharField(max_length=300, null=True)
    start_date =  models.DateField(auto_now_add=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    
    def __str__(self) -> str:
        return f"(BUSINESS-SHOW{self.name},  {self.description}"

class BusinessTrivial(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, null=False)
    description = models.CharField(max_length=200, null=True)
    is_active = models.BooleanField(default=True)
    total_points = models.IntegerField()
    start_at = models.DateTimeField(default=timezone.now)



