from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import json
from django.http import JsonResponse, HttpResponse
from userpreferences.models import UserPreference
import datetime
import csv
import xlwt

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
    currency = UserPreference.objects.get(user=request.user).currency
    context = {
       "expenses":expenses,
       "page_obj":page_obj,
       "currency":currency
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

def expense_category_summary(request):
   todays_date = datetime.date.today()
   six_month_ago = todays_date-datetime.timedelta(days=30*6)
   # Filter expenses within the last six months
   expenses = Expense.objects.filter(
      owner = request.user, date__gte = six_month_ago,date__lte=todays_date
   )
   finalrep = {}
   def get_category(expense):
      return expense.category
   category_list = list(set(map(get_category,expenses)))
   def get_expenses_category_amount(category):
      amount = 0
      filtered_by_category = expenses.filter(category=category)
      for item in filtered_by_category:
         amount += item.amount
      return amount
   for x in expenses:
      for y in category_list:
         finalrep[y] = get_expenses_category_amount(y)
   return JsonResponse({'expense_category_data': finalrep}, safe=False)

def stats_view(request):
   return render(request,"expenses/stats.html")

def export_csv(request):
   response = HttpResponse(content_type='text/csv')
   response['Content-Disposition'] = 'attachment; filename+Expenses'+ str(datetime.datetime.now()) + '.csv'
   
   writer = csv.writer(response)
   writer.writerow(['Amount',"Description","Category","Date"])
   expenses = Expense.objects.filter(owner=request.user)
   for expense in expenses:
      writer.writerow([expense.amount,expense.description,expense.category,expense.date])
   return response

def export_excel(request):
   response = HttpResponse(content_type='application/ms-excel')
   response['Content-Disposition'] = 'attachment; filename+Expenses'+ str(datetime.datetime.now()) + '.xls'
   
   wb = xlwt.Workbook(encoding='utf-8')
   ws = wb.add_sheet('Expenses')
   row_num = 0
   font_sytle = xlwt.XFStyle()
   font_sytle.font.bold = True
   columns = ['Amount',"Description","Category","Date"]
   for col_num in range(len(columns)):
      ws.write(row_num,col_num,columns[col_num],font_sytle)
   font_sytle = xlwt.XFStyle()

   rows = Expense.objects.filter(owner = request.user).values_list("amount","description","category","date")

   for row in rows:
      row_num += 1
      for col_num in range(len(row)):
         ws.write(row_num,col_num,str(row[col_num]),font_sytle)
   wb.save(response)
   return response












   