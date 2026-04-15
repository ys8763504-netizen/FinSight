from django.shortcuts import render, redirect
from .models import reg_users, Expense, Budget, Category, Feedback, Goal
from django.db.models import Sum
from django.http import JsonResponse
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime, date

# Create your views here.
def home_page(request):
    return render(request, "home.html")
def index_page(request):
   
   if 'login' in request.session:
       return render(request,'index.html',{'login':True})
   else:
       return render(request,'index.html',{'login':False})       

def login_form(request):
    if request.method == 'POST':
        try:
            registered= reg_users.objects.get(email=request.POST.get('email'))
            if registered.password == request.POST.get('password'):
                request.session['login'] = registered.email
                request.session['user_id'] = registered.id
                return render(request,'index.html',{'login':True})
            else:
                return render(request,'login.html',{'check_pass':'Password is wrong.'})
        except:
            return render(request,'login.html',{'registered':'Email is not registered.'})
    else:
       return render(request,'login.html')
    
def user_logout(request):
    del request.session['login']
    return redirect('index_page')

def regis_form(request):
    if request.method == 'POST':
        user_obj=reg_users()
        user_obj.name = request.POST.get('name')
        user_obj.mobile = request.POST.get('mobile')
        user_obj.email = request.POST.get('email')
        user_obj.password = request.POST.get('password')
        user_obj.gender = request.POST.get('gender')
        user_obj.date_of_birth = request.POST.get('dob')
        user_obj.country = request.POST.get('country')
        user_obj.terms = request.POST.get('terms', False)
        already_reg= reg_users.objects.filter(email=user_obj.email)
        if already_reg:
            return render(request,'registration.html',{'already':'Email is already registered.'})
        else:
            user_obj.save()
            return redirect('login_form')
    else:
        return render(request,'registration.html')
    
def about_page(request):
    if 'login' in request.session:
       return render(request,'about.html',{'login':True})
    else:
       return render(request,'about.html',{'login':False})

def profile_page(request):
    if 'login' in request.session:
        user_id = request.session.get('user_id')
        user = reg_users.objects.get(id=user_id)

        context={
            "user": user,
            'login':True
        }
        return render(request, "profile.html", context)
    else:
        return render(request, 'index.html',{'loged_out':'you have to login first'}) 

def update_profile(request):
    if request.method == "POST":

        user_id = request.session.get('user_id')
        user = reg_users.objects.get(id=user_id)

        user.name = request.POST.get('name')
        user.mobile = request.POST.get('mobile')
        user.gender = request.POST.get('gender')
        user.date_of_birth = request.POST.get('date_of_birth')
        user.country = request.POST.get('country')

        user.save()

        return redirect('profile_page')  
def change_password(request):
    if request.method == "POST":

        user_id = request.session.get('user_id')
        user = reg_users.objects.get(id=user_id)

        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # ✅ Check old password
        if old_password != user.password:
            messages.error(request, "Old password is incorrect!")
            return redirect('profile_page')
        if new_password != confirm_password:
            messages.error(request, "Confirm Password is not Maching!")
            return redirect('profile_page')

        # ✅ Save new password (hashed)
        user.password = new_password
        user.save()

        messages.success(request, "Password updated successfully!")

        return redirect('profile_page')                  

def dashboard_page(request):
    if 'login' in request.session:
        user_id = request.session.get('user_id')

        expenses = Expense.objects.filter(user_id=user_id)

        # This Month Expense
        current_month = datetime.now().month
        this_month_expense = expenses.filter(date__month=current_month).aggregate(Sum('amount'))['amount__sum'] or 0

        # Total Expense
        total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0


        # Current date
        now = datetime.now()

        current_month_year = now.strftime("%Y-%m")

        budget = Budget.objects.filter(
                user_id=user_id,
                month=current_month_year
            )
        total_budget = budget.aggregate(Sum('amount'))['amount__sum'] or 0
        print(budget)
        remaining=total_budget-this_month_expense
        
        

        # Recent Transactions (last 5)
        recent_expenses = expenses.order_by('-date')[:5]

        # Category-wise data for chart
        category_data = expenses.values('category').annotate(total=Sum('amount'))

        labels = [item['category'] for item in category_data]
        data = [item['total'] for item in category_data]

        context = {
            'total_expense': total_expense,
            'this_month_expense': this_month_expense,
            'remaining_budget': remaining,
            'recent_expenses': recent_expenses,
            'labels': labels,
            'data': data,
            'login':True
        }

        return render(request, 'dash.html', context)
    else:
        return render(request, 'index.html',{'loged_out':'you have to login first'})
def add_expense(request):
    if request.method == "POST":

            user_id = request.session.get('user_id')
            user = reg_users.objects.get(id=user_id)

            title = request.POST.get('title')
            category = request.POST.get('category')
            date = request.POST.get('date')

            # ✅ Convert amount properly
            amount = float(request.POST.get('amount'))

            # ✅ Convert date
            date_obj = datetime.strptime(date, "%Y-%m-%d")

            # ✅ Get month-year format
            month_year = date_obj.strftime("%Y-%m")

            # ✅ Get budget (ONLY ONCE, correct way)
            budget = Budget.objects.filter(
                month=month_year
            ).first()

            # ✅ Get budget for this user and month
            budget = Budget.objects.filter(
                user_id=user,
                month=month_year
            ).first()

            # ❌ If no budget exists
            if not budget:
                messages.error(
                    request,
                    f"Budget is not set for ({month_year}). Please add budget."
                )
                return redirect('expense_page')

            budget_amount = float(budget.amount)

            # ✅ Total spent for same month 
            total_spent = Expense.objects.filter(
                user_id=user,
                date__year=date_obj.year,
                date__month=date_obj.month
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            print()
            new_total = total_spent + amount

            # 🚨 Budget check
            if new_total > budget_amount:
                messages.error(request, f"Budget exceeded for this month! ({month_year})")

            # ✅ Save expense
            Expense.objects.create(
                user_id=user,
                title=title,
                amount=amount,   
                category=category,
                date=date_obj
                )

            messages.success(request, "Expense added successfully!")
            return redirect('expense_page')
    
def expense_page(request):
    if 'login' in request.session:
    
        user_id = request.session.get('user_id')

        expenses = Expense.objects.filter(user_id=user_id)
        categories = Category.objects.filter(user=user_id)

        total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

        return render(request,'expense.html',{
            'expenses':expenses,
            'total_expense':total_expense,
            "categories": categories,
            'login':True
        })
    else:
        return render(request, 'index.html',{'loged_out':'you have to login first'}) 
    
def edit_expense(request,id):

    user_id = request.session.get('user_id')
    expense = Expense.objects.get(id=id)
    category=Category.objects.filter(user=user_id)
    context={
        'category':category,
        'expense':expense
    }
    return render(request,'edit_expense.html',context)
    
def update_expense(request,id):

    expense = Expense.objects.get(id=id)

    if request.method == "POST":

        expense.title = request.POST.get('title')
        expense.amount = request.POST.get('amount')
        expense.category = request.POST.get('category')
        expense.date = request.POST.get('date')

        expense.save()

        return redirect('expense_page')

def delete_expense(request, id):

    expense = Expense.objects.get(id=id)

    expense.delete()

    return redirect('expense_page')

def budget_page(request):
    if 'login' in request.session:
        user_id = request.session.get('user_id')
        budgets = Budget.objects.filter(user_id=user_id)
        expenses = Expense.objects.filter(user_id=user_id)

        total_budget = sum(b.amount for b in budgets)
        categories = Category.objects.filter(user=user_id)
        total_budget = budgets.aggregate(Sum('amount'))['amount__sum'] or 0
        total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        remaining = total_budget - total_expense

        context = {
            "budgets": budgets,
            "total_budget": total_budget,
            "total_expense": total_expense,
            "remaining": remaining,
            "categories": categories,
            'login':True
        }
        return render(request,"budget.html",context)
    else:
        return render(request, 'index.html',{'loged_out':'you have to login first'}) 

from django.shortcuts import redirect, render
from django.contrib import messages
from datetime import datetime

def add_budget(request):

    user_id = request.session.get('user_id')

    if request.method == "POST":

        user = reg_users.objects.get(id=user_id)
        title = request.POST.get("title")
        amount = request.POST.get("amount")
        month = request.POST.get("month")   # format: "YYYY-MM"

        # ✅ split input month
        input_year, input_month = map(int, month.split('-'))

        # ✅ current date
        now = datetime.now()
        current_year = now.year
        current_month = now.month

        # -------------------------------
        # ❌ Case 1: Past month
        # -------------------------------
        if (input_year < current_year) or (
            input_year == current_year and input_month < current_month
        ):
            messages.error(request, "You cannot add budget for past months.")
            return redirect("budget_page")

        # -------------------------------
        # ⚠ Case 2: Future month
        # -------------------------------
        elif (input_year > current_year) or (
            input_year == current_year and input_month > current_month
        ):
            messages.warning(request, "Budget added! But You cannot add expenses for future months.")
            Budget.objects.create(
            user_id=user,
            title=title,
            amount=amount,
            month=month
            )
            return redirect("budget_page")
        # -------------------------------
        # ✅ Case 3: Current month
        # -------------------------------

        elif Budget.objects.filter(user_id=user, month=month).exists():
            messages.error(request, "Budget for this month already exists.")
            return redirect("budget_page")
        
        else:
            messages.success(request, "Budget added for current month.")
            Budget.objects.create(
            user_id=user,
            title=title,
            amount=amount,
            month=month
            )

            return redirect("budget_page")
        # ✅ Save budget
        

    return render(request, "add_budget.html")
def edit_budget(request,id):

    budget = Budget.objects.get(id=id)

    return render(request,'edit_budget.html',{'budget':budget})
    
def update_budget(request,id):

    budget = Budget.objects.get(id=id)

    if request.method == "POST":

        budget.title = request.POST.get('title')
        budget.amount = request.POST.get('amount')
        budget.month = request.POST.get('month')

        budget.save()

        return redirect('budget_page')

def delete_budget(request, id):

    buget = Budget.objects.get(id=id)

    buget.delete()

    return redirect('budget_page')

def report_page(request):
    if 'login' in request.session:
        user_id = request.session.get('user_id')
        budgets = Budget.objects.filter(user_id=user_id)
        expenses = Expense.objects.filter(user_id=user_id)

        total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        total_budget = budgets.aggregate(Sum('amount'))['amount__sum'] or 0
        remaining = total_budget - total_expense
        total_transactions = expenses.count()
        now = datetime.now()


        category_report = expenses.values('category').annotate(total=Sum('amount'))

        monthly_report = expenses.extra(
            select={'month':"strftime('%%m',date)"}
        ).values('month').annotate(total=Sum('amount'))

        budget_report = []

        for budget in budgets:
            year, month = budget.month.split('-')
            spent = expenses.filter(
                date__year=int(year),
                date__month=int(month)
            ).aggregate(
                Sum('amount')
            )['amount__sum'] or 0

            remaining_budget = budget.amount - spent

            budget_report.append({
                "title":budget.title,
                "amount":budget.amount,
                "month":budget.month,
                "spent":spent,
                "remaining":remaining_budget
            })

        context={
            "total_expense":total_expense,
            "total_budget":total_budget,
            "remaining":remaining,
            "total_transactions":total_transactions,
            "category_report":category_report,
            "monthly_report":monthly_report,
            "budget_report":budget_report,
            'login':True
        }

        return render(request,"report.html",context)
    else:
        return render(request, 'index.html',{'loged_out':'you have to login first'}) 

def analytics_page(request):
    if 'login' in request.session:
        user_id = request.session.get('user_id')
        budgets = Budget.objects.filter(user_id=user_id)
        expenses = Expense.objects.filter(user_id=user_id)
        category_data = expenses.values('category').annotate(total=Sum('amount'))

        monthly_data =expenses.extra(
            select={'month':"strftime('%%m',date)"}
        ).values('month').annotate(total=Sum('amount'))

        total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        total_budget = budgets.aggregate(Sum('amount'))['amount__sum'] or 0
        total_transactions =expenses.count()

        top_category = expenses.values('category').annotate(
            total=Sum('amount')
        ).order_by('-total').first()

        context = {
            "category_data": list(category_data),
            "monthly_data": list(monthly_data),
            "total_expense": total_expense,
            "total_budget": total_budget,
            "total_transactions": total_transactions,
            "top_category": top_category,
            'login':True
        }

        return render(request,"analytics.html",context)
    else:
        return render(request, 'index.html',{'loged_out':'you have to login first'}) 
def check_budget(request):
    category = request.GET.get('category')
    month = request.GET.get('month')

    budget = Budget.objects.filter(
        category__iexact=category,
        month=month
    ).first()

    if not budget:
        return JsonResponse({'budget': False})

    # Calculate spent
    year, mon = month.split('-')

    total_spent = Expense.objects.filter(
        category__iexact=category,
        date__year=year,
        date__month=mon
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    remaining = float(budget.amount) - total_spent

    return JsonResponse({
        'budget': True,
        'remaining': remaining
    })
def category_page(request):
    user_id = request.session.get('user_id')
    cat=Category.objects.filter(user=user_id)
    context={
        "categories": cat,
         'login':True
    }
    return render(request,"category.html",context)

def add_category(request):
    user_id = request.session.get('user_id')
    user = reg_users.objects.get(id=user_id)

    if request.method == "POST":
        name = request.POST.get('name')

        if not name:
            messages.success(request, "Please Enter Category")
            return redirect("category_page")

        # duplicate
        if Category.objects.filter(user=user, name__iexact=name).exists():
            messages.success(request, "Category Already Exist")
            return redirect("category_page")

        Category.objects.create(user=user, name=name)
        return redirect("category_page")
    return redirect("category_page")  

def delete_category(request, id):
    Category.objects.get(id=id).delete()
    return redirect('category_page')
   
def feedback_page(request):
   
   if 'login' in request.session:
    
        feedbacks = Feedback.objects.order_by('-created_at')[:5]
        context={
            'login':True,
            "feedbacks":feedbacks
        }
        return render(request,'feedback.html',context)
   else:
        feedbacks = Feedback.objects.order_by('-created_at')[:5]
        context={
            'login':False,
            "feedbacks":feedbacks
        }
        return render(request,'feedback.html',context)
   
def add_feedback(request):

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        type = request.POST.get("type")
        message = request.POST.get("message")
        rating = request.POST.get("rating")

        if not name or not email or not message or not type or not rating:
            messages.error(request, "All fields are required")
            return redirect("feedback")

        Feedback.objects.create(
            name=name,
            email=email,
            type=type,
            message=message,
            rating=rating
        )

        messages.success(request, "Thank you for your feedback! ⭐")
        return redirect("feedback")
    
    return redirect("feedback")
def admin_login_page(request):
    return render(request, "admin_panel/admin_login.html")
def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid admin credentials")

    return render(request, "admin_panel/admin_login.html")

def admin_logout(request):
    if request.user.is_authenticated:
        logout(request) 
    return redirect('admin_login_page')

def admin_check(user):
    return user.is_staff

@login_required
@user_passes_test(admin_check)
def admin_dashboard(request):
    users = reg_users.objects.all()
    expenses = Expense.objects.all()
    budgets = Budget.objects.all()
    feedbacks = Feedback.objects.all()
    category = Category.objects.all()

    context = {
        "users": users,
        "expenses": expenses,
        "budgets": budgets,
        "feedbacks": feedbacks,
        "category":category,
    }
    return render(request, "admin_panel/dashboard.html", context)

# DELETE USER
@login_required
@user_passes_test(admin_check)
def delete_user(request, id):
    reg_users.objects.get(id=id).delete()
    return redirect('admin_dashboard')


# EDIT USER PAGE
@login_required
@user_passes_test(admin_check)
def edit_user(request, id):
    user = reg_users.objects.get(id=id)
    return render(request, 'admin_panel/edit_user.html', {"user": user})


# UPDATE USER
@login_required
@user_passes_test(admin_check)
def update_user(request, id):
    user = reg_users.objects.get(id=id)

    if request.method == "POST":
        user.name = request.POST.get('name')
        user.mobile = request.POST.get('mobile')
        user.email = request.POST.get('email')
        user.gender = request.POST.get('gender')
        user.date_of_birth = request.POST.get('date_of_birth')
        user.country = request.POST.get('country')

        user.save()
        messages.success(request, "User updated successfully!")

        return redirect('admin_dashboard')

@login_required
@user_passes_test(admin_check)
def admin_delete_expense(request, id):
    Expense.objects.get(id=id).delete()
    return redirect('admin_dashboard')


@login_required
@user_passes_test(admin_check)
def admin_edit_expense(request, id):
    expense = Expense.objects.get(id=id)
    return render(request, 'admin_panel/edit_expense.html', {"expense": expense})


@login_required
@user_passes_test(admin_check)
def admin_update_expense(request, id):
    expense = Expense.objects.get(id=id)

    if request.method == "POST":
        expense.title = request.POST.get('title')
        expense.amount = request.POST.get('amount')
        expense.category = request.POST.get('category')
        expense.date = request.POST.get('date')
        expense.save()

    return redirect('admin_dashboard')

@login_required
@user_passes_test(admin_check)
def admin_delete_budget(request, id):
    Budget.objects.get(id=id).delete()
    return redirect('admin_dashboard')


@login_required
@user_passes_test(admin_check)
def admin_edit_budget(request, id):
    budget = Budget.objects.get(id=id)
    return render(request, 'admin_panel/edit_budget.html', {"budget": budget})


@login_required
@user_passes_test(admin_check)
def admin_update_budget(request, id):
    budget = Budget.objects.get(id=id)

    if request.method == "POST":
        budget.title = request.POST.get('title')
        budget.amount = request.POST.get('amount')
        budget.month = request.POST.get('month')
        budget.save()

    return redirect('admin_dashboard')

@login_required
@user_passes_test(admin_check)
def delete_feedback(request, id):
    Feedback.objects.get(id=id).delete()
    return redirect('admin_dashboard')

@login_required
@user_passes_test(admin_check)
def admin_delete_category(request, id):
    Category.objects.get(id=id).delete()
    return redirect('admin_dashboard')

def goal_page(request):
    user_id = request.session.get('user_id')
    goals = Goal.objects.filter(user_id=user_id)
    context={
        "goals": goals,
        "login":True
    }
    return render(request, "goal.html", context)


def add_goal(request):
    if request.method == "POST":
        user_id = request.session.get('user_id')
        goal_date = request.POST.get("date")

        date_obj = datetime.strptime(goal_date, "%Y-%m-%d").date()

        if date_obj < date.today():
            messages.error(request, "You cannot select a past date")
            return redirect("goal_page")
        
        Goal.objects.create(
            user_id=user_id,
            title=request.POST.get("title"),
            target_amount=request.POST.get("target"),
            target_date=request.POST.get("date")
        )

        return redirect("goal_page")


def add_saving(request, id):
    goal = Goal.objects.get(id=id)

    if request.method == "POST":
        amount = float(request.POST.get("amount"))

        if amount <= 0:
            messages.error(request, "Amount must be greater than 0")
            return redirect("goal_page")

        if goal.is_completed:
            messages.error(request, "Goal already achieved 🎉")
            return redirect("goal_page")

        goal.saved_amount += amount

        if goal.saved_amount >= goal.target_amount:
            goal.saved_amount = goal.target_amount
            goal.is_completed = True
            messages.success(request, "🎉 Congratulations! Goal Achieved!")

        goal.save()
        return redirect("goal_page")

from django.shortcuts import get_object_or_404

def delete_goal(request, id):
    goal = get_object_or_404(Goal, id=id)

    goal.delete()
    return redirect("goal_page")

from .utils.ai_insights import generate_insights

from .models import Goal

def ai_dashboard(request):
    if 'login' in request.session:
        user_id = request.session.get('user_id')

        expenses = Expense.objects.filter(user_id=user_id)
        budgets = Budget.objects.filter(user_id=user_id)
        goals = Goal.objects.filter(user_id=user_id)

        # Total expense
        total = expenses.aggregate(total=Sum('amount'))['total'] or 0

        # Category data
        category_data = expenses.values('category').annotate(total=Sum('amount'))
        categories = {item['category']: item['total'] for item in category_data}

        # Budget data
        budget_data = {b.month: b.amount for b in budgets}

        # Goals data
        goals_data = [
            {
                "title": g.title,
                "target": g.target_amount,
                "saved": g.saved_amount,
                "remaining": g.target_amount - g.saved_amount
            }
            for g in goals
        ]

        # Expense list
        expense_list = list(expenses.values('title', 'amount', 'category'))

        insights = generate_insights(
            expense_list,
            total,
            categories,
            budget_data,
            goals_data
        )
        insights = insights.replace("**","")
        
        insights = insights.replace("*","•")
        return render(request, 'ai_dashboard.html', {
            'insights': insights,
            'total': total,
            'categories': categories,
            'login' : True
        })
    else:
        return render(request, 'index.html',{'loged_out':'you have to login first'})
from .utils.ai_chat import generate_chat_reply
from django.http import JsonResponse
import json
from .utils.ai_insights import generate_insights

def ai_chat(request):
    if request.method == "POST":

        try:
            data = json.loads(request.body)
            user_message = data.get("message")

            
            user_id = request.session.get("user_id")

            if not user_id:
                return JsonResponse({"reply": "Please login first."})

           
            expenses = Expense.objects.filter(user_id=user_id)

            total_expense = expenses.aggregate(
                total=Sum('amount')
            )['total'] or 0

            category_data = expenses.values('category').annotate(
                total=Sum('amount')
            )

            categories = {
                item['category']: item['total']
                for item in category_data
            }

            
            budgets = Budget.objects.filter(user_id=user_id)

            total_budget = budgets.aggregate(
                total=Sum('amount')
            )['total'] or 0

           
            goals = Goal.objects.filter(user_id=user_id)

            goal_data = []
            for g in goals:
                goal_data.append({
                    "title": g.title,
                    "target": float(g.target_amount),
                    "saved": float(g.saved_amount),
                    "completed": g.is_completed
                })

        
            reply = generate_chat_reply(
                user_message,
                total_expense,
                categories,
                total_budget,
                goal_data
            )

            return JsonResponse({"reply": reply})

        except Exception as e:
            return JsonResponse({"reply": f"Error: {str(e)}"})

    return JsonResponse({"reply": "Invalid request"})