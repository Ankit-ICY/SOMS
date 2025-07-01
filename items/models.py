from django.db import models
from company.models import Company
from users.models import BaseModel
from users.models import CustomUser

class FoodCategory(BaseModel): #Dal, Rice, Roti 
    name = models.CharField(max_length=200)
    description = models.TextField()

class FoodItem(BaseModel):
    class FoodVisibility(models.TextChoices):
        PUBLIC = 'public', 'Public'
        PRIVATE = 'private', 'Private'

    class FoodGroupChoices(models.TextChoices):
        FOOD = 'food', 'Food'
        DRINK = 'drink', 'Drink'
        DESSERT = 'dessert', 'Dessert'

    class FoodTypeChoices(models.TextChoices):
        VEG = 'veg', 'Veg'
        NON_VEG = 'non_veg', 'Non-Veg'
        VEGAN = 'vegan', 'Vegan'

    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='food_items')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='food_items/', null=True, blank=True)
    category = models.ForeignKey(FoodCategory,on_delete=models.SET_NULL, blank=True,null=True)
    group = models.CharField(max_length=20, choices=FoodGroupChoices.choices)
    food_type = models.CharField(max_length=20, choices=FoodTypeChoices.choices)
    visibility = models.CharField(max_length=20, choices=FoodVisibility.choices, default=FoodVisibility.PUBLIC)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    

class CompanyFoodItem(BaseModel):
    class SpecialTags(models.TextChoices):
        NONE = 'none', 'None'
        SPECIAL = 'special', 'Chef Special'
        DAY = 'food_of_day', 'Food of the Day'
        LIMITED = 'limited', 'Limited Edition'

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_items')
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE, related_name='item_companies')
    
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)
    special_tag = models.CharField(
        max_length=20,
        choices=SpecialTags.choices,
        default=SpecialTags.NONE
    )
    special_note = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = ('company', 'food_item')

    def __str__(self):
        return f"{self.food_item.name} at {self.company.name} - ₹{self.price}"
