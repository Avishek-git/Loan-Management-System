from django.utils import timezone
from django.db import models
from loanApplication.models import Loan

class Payment(models.Model):
    #loan = models.ForeignKey('Loan', on_delete=models.CASCADE)
    Loan_id = models.PositiveIntegerField()
    Amount = models.DecimalField(max_digits=10, decimal_places=2)
    Payment_date = models.DateField(default=timezone.now)

    
    def __str__(self):
        #return f"Payment ID: {self.id}, Loan: {self.loan}, Amount: {self.amount}, Date: {self.payment_date}"
        return f"Loan ID: {self.Loan_id} Amount: {self.Amount}, Date: {self.Payment_date}"

