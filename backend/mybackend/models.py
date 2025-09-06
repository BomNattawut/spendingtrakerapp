
from django.db import models
from django.contrib.auth.models import User

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Expense(models.Model):
    expenseid = models.AutoField(primary_key=True)  # หรือใช้ IntegerField() แทน
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.ForeignKey(ExpenseCategory, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.description} - {self.amount}"

class Budget(models.Model):
    budgetid = models.AutoField(primary_key=True)  # หรือใช้ IntegerField() แทน
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.description} - {self.amount}"


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pictureid=models.AutoField(primary_key=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return self.user.username

