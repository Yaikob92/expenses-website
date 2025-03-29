from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
# Create your views here.

def search_expenses(request):
  if request.method == "POST":
      search_str = json.loads(request.body).get('searchText')
      expenses = Expense.objects.filter(
        amount__istartswith=search_str,owner=request.user) | Expense.objects.filter(
        date__istartswith=search_str,owner=request.user) | Expense.objects.filter(
        description__icontains=search_str,owner=request.user) | Expense.objects.filter(
        category__icontains=search_str,owner=request.user)
      data = expenses.values()
      return JsonResponse(list(data),safe=False)



@login_required(login_url="authentication/login")
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses,5)
    page_number  = request.GET.get("page")
    page_obj = Paginator.get_page(paginator,page_number)
    context = {
       "expenses":expenses,
       "page_obj":page_obj
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
      return render(request,"expenses/edit-expenses.html",context)
    description = request.POST['description']
    date = request.POST['expense_date']
    category = request.POST['category']

    if not description:
      messages.error(request,"description is required")
      return render(request,"expenses/edit-expenses.html",context)
    expenses.owner=request.user
    expenses.date=date
    expenses.amount=amount
    expenses.category=category
    expenses.description=description
    expenses.save()
    messages.success(request,"Expenses Updated  successfully")
    return redirect("expenses")
   

def delete_expense(request, id):
  expense = Expense.objects.get(pk=id)
  expense.delete()
  messages.success(request,"Expenses removed")
  return redirect("expenses")






















   