from django.contrib import admin
from .models import reg_users, Expense, Budget, Category, Feedback, Goal
# Register your models here.
admin.site.register(reg_users)
admin.site.register(Expense)
admin.site.register(Budget)
admin.site.register(Category)
admin.site.register(Feedback)
admin.site.register(Goal)