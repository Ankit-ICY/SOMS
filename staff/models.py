from users.models import BaseModel, CustomUser
from company.models import Company
from django.db import models


class CompanyStaff(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='staff_members')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assigned_companies')
    assigned_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='staff_created')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('company', 'user')

    def __str__(self):
        return f"{self.user.name} - {self.company.name}"