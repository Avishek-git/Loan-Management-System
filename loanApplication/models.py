from django.db import models
from django.utils import timezone
import types

class Loan(models.Model):
    LOAN_TYPES = (
        ('Car', 'Car Loan'),
        ('Home', 'Home Loan'),
        ('Education', 'Education Loan'),
        ('Personal', 'Personal Loan'),
    )

    uuid = models.CharField(max_length=100)
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPES)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    term_period = models.PositiveIntegerField() 
    disbursement_date = models.DateField(default=timezone.now)
    emi_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_amount_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20,default="OPEN")
    # due_dates = models.JSONField(null=True, blank=True)
 
    
    def __str__(self):
        return f"Loan ID: {self.id}, User ID: {self.uuid}, Type: {self.loan_type}"

