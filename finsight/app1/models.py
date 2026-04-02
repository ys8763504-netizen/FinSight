from django.db import models
# Create your models here.
class reg_users(models.Model):
    name = models.CharField(max_length=100) 
    mobile = models.CharField(max_length=15) 
    email = models.EmailField(unique=True) 
    password = models.CharField(max_length=255) 
    gender = models.CharField(max_length=10, choices=[('Male','Male'), ('Female','Female'), ('Other','Other')]) 
    date_of_birth = models.DateField()
    country=models.CharField(max_length=50) 
    terms = models.BooleanField(default=False)
    registered_at = models.DateTimeField(auto_now_add=True)  
    def __str__(self): 
        return self.name
    
class Expense(models.Model):

    user_id = models.ForeignKey(reg_users, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    amount = models.IntegerField()
    category = models.CharField(max_length=50)
    date = models.DateField()

    def __str__(self):
        return self.title

class Budget(models.Model):

    user_id = models.ForeignKey(reg_users, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    amount = models.IntegerField()

    month = models.CharField(max_length=7)

    def __str__(self):
        return self.title

class Category(models.Model):
    user = models.ForeignKey(reg_users, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    type = models.CharField(max_length=20)
    message = models.TextField()
    rating = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
from datetime import date

class Goal(models.Model):
    user = models.ForeignKey('reg_users', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    target_amount = models.FloatField()
    saved_amount = models.FloatField(default=0)
    target_date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    def progress(self):
        if self.target_amount == 0:
            return 0
        return int((self.saved_amount / self.target_amount) * 100)

    def remaining_amount(self):
        return max(self.target_amount - self.saved_amount, 0)

    def months_left(self):
        if not self.target_date:
            return 0

        today = date.today()
        months = (self.target_date.year - today.year) * 12 + (self.target_date.month - today.month)

        return max(months, 1)  # avoid divide by 0

    def avg_saving_per_month(self):
        remaining = self.remaining_amount()
        months = self.months_left()

        if months == 0:
            return remaining

        return round(remaining / months, 2)