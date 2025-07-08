# company/models.py
from django.db import models
from users.models import CustomUser
import uuid

class Company(models.Model):
    class CompanyChoices(models.TextChoices):
        CAFE = 'cafe' , 'CAFE',
        RESTAURANT = 'restaurant', 'RESTAURANT'

    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='companies')
    name = models.CharField(max_length=255)
    company_type = models.CharField(max_length=50, choices=CompanyChoices.choices, default=CompanyChoices.CAFE)
    gst_number = models.CharField(max_length=15, blank=True, null=True)
    fssai_license = models.CharField(max_length=14, blank=True, null=True)
    
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    staff = models.ManyToManyField(CustomUser, related_name="company_staff")
    logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    url= models.URLField()
    qr_code_image = models.ImageField(upload_to='qr_codes/', null=True, blank=True)

    def __str__(self):
        return self.name
