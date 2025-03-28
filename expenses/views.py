from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages

# Create your views here.
@login_required(login_url="authentication/login")
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    context = {
       "expenses":expenses
    }
    return render(request,"expenses/index.html",context)
def add_expense(request):
    categories = Category.objects.all()
    context = {
      "categories":categories,
      "value":request.POST
    }
    if request.method == "GET":
      return render(request,"expenses/add_expenses.html",context)
    if request.method == "POST":
      amount = request.POST['amount']
      if not amount:
        messages.error(request,"Amount is required")
        return render(request,"expenses/add_expenses.html",context)
      description = request.POST['description']
      date = request.POST['expense_date']
      category = request.POST['category']

      if not description:
        messages.error(request,"description is required")
        return render(request,"expenses/add_expenses.html",context)
      Expense.objects.create(owner=request.user,date=date, amount=amount, category=category,description=description)
      messages.success(request,"Expenses saved successfully")
      return redirect("expenses")

def expense_edit(request,id):
   expenses = Expense.objects.get(pk=id)
   categories = Category.objects.all()

   context = {
      "expenses":expenses,
      "value":expenses,
      "categories":categories
   }
   if request.method == "GET":
      return render(request,"expenses/edit-expenses.html",context)
   if request.method == "POST":
    amount = request.POST['amount']
    if not amount:
      messages.error(request,"Amount is required")
      return render(request,"expenses/edit_expenses.html",context)
    description = request.POST['description']
    date = request.POST['expense_date']
    category = request.POST['category']

    if not description:
      messages.error(request,"description is required")
      return render(request,"expenses/edit_expenses.html",context)
    expenses.owner=request.user,
    expenses.date=date,
    expenses.amount=amount, 
    expenses.category=category,
    expenses.description=description
    expenses.save()
    messages.success(request,"Expenses Updated  successfully")
    return redirect("expenses")