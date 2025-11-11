class LoanCategory(models.Model):
    loan_name = models.CharField(max_length=100)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="Enter interest rate (e.g. 8.50 for 8.5%)")

    def __str__(self):
        return f"{self.loan_name} ({self.interest_rate}%)"
