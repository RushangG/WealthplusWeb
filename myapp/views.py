from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from .forms import SignupForm, LoginForm
from .models import UserProfile
from .models import Income
from .models import Expense,Report 
from django.http import HttpResponse
from django.shortcuts import render
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Image
from django.contrib.auth.decorators import login_required
import datetime
from django.db.models import Min, Max
from django.utils import timezone


def home(request):
    return render(request, 'home.html')


def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Save form data
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})



# login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


def income(request):
    if request.method=='POST':
        source=request.POST['source']
        amount=request.POST['amount']
        date=request.POST['date']
        category=request.POST['category']
        formtype=request.POST['formtype']
        #print(formtype)
        if formtype=='update':
            id=request.POST['incomeid']
            income=Income.objects.all().filter(id=id,user=request.user)
            if not income:
                 return HttpResponse("Income not found", status=404)
            else:
              obj=income[0]
              obj.category=category
              obj.amount=amount
              obj.date=date
              obj.source=source
              obj.save()
              return redirect('income')
        else:
            income=Income(source=source,amount=amount,date=date,category=category,user=request.user)
            income.save()
            return redirect('income')



    incomes = Income.objects.all().filter(user=request.user)
    
    return render(request, 'income.html', {'incomes': incomes})


def deleteIncome(request):
    incomeId=request.GET['incomeid']
    income=Income.objects.all().filter(id=incomeId,user=request.user)
    if not income:
        return HttpResponse("Income not found", status=404)
    income=income[0]
    if income.user==request.user:
        income.delete()
    else:
        return HttpResponse("You can not Delete this Income", status=401)
    
    return redirect('income')


def expense(request):
    if request.method=='POST':
        name=request.POST['name']
        amount=request.POST['amount']
        date=request.POST['date']
        category=request.POST['category']
        formtype=request.POST['formtype']
        print(formtype)
        if formtype=='update':
            id=request.POST['expenseid']
            expense=Expense.objects.all().filter(id=id,user=request.user)
            if not income:
                 return HttpResponse("Expense not found", status=404)
            else:
              obj=expense[0]
              obj.category=category
              obj.amount=amount
              obj.date=date
              obj.name=name
              obj.save()
              return redirect('expense')
        else:
            expense=Expense(name=name,amount=amount,date=date,category=category,user=request.user)
            expense.save()
            return redirect('expense')



    expenses = Expense.objects.all().filter(user=request.user)
    
    
    return render(request, 'expense.html', {'expenses': expenses})


def deleteExpense(request):
    expenseId=request.GET['expenseid']
    expense=Expense.objects.all().filter(id=expenseId,user=request.user)
    if not expense:
        return HttpResponse("Expense not found", status=404)
    expense=expense[0]
    if expense.user==request.user:
        expense.delete()
    else:
        return HttpResponse("You can not Delete this Expense", status=401)
    

    return redirect('expense')


def report(request):
        
        expenses = Expense.objects.all().filter(user=request.user)
        incomes = Income.objects.all().filter(user=request.user)

        total_income = sum(income.amount for income in incomes)
        total_expense = sum(expense.amount for expense in expenses)
        profit = total_income - total_expense
        # Calculate the value based on the formula provided
        if total_income + total_expense != 0:
            value = (total_income / (total_income + total_expense)) * 100
        else:
            value = -1

        return render(request, 'report.html', {'incomes': incomes, 'expenses': expenses, 'total_incomes': total_income, 'total_expense': total_expense, 'profit': profit, 'value': value})



def generate_pdf(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if (not start_date) and (not end_date) :
            min_income_date = Income.objects.aggregate(min_date=Min('date'))['min_date']
          
            min_expense_date = Expense.objects.aggregate(min_date=Min('date'))['min_date']
          
            max_income_date = Income.objects.aggregate(max_date=Max('date'))['max_date']
           
            max_expense_date = Expense.objects.aggregate(max_date=Max('date'))['max_date']
            
            # Determine the overall minimum start date
            if min_income_date and min_expense_date:
                start_date = min(min_income_date, min_expense_date)
            elif min_income_date:
                start_date = min_income_date
            else:
                start_date = min_expense_date
            if max_income_date and max_expense_date:
                end_date = max(max_income_date, max_expense_date)
            elif max_income_date:
                end_date = max_income_date
            else:
                end_date = max_expense_date
            
            # Convert start_date and end_date to strings in 'YYYY-MM-DD' format
            start_date = start_date.strftime('%Y-%m-%d') if start_date else ''
            end_date = end_date.strftime('%Y-%m-%d') if end_date else ''
            
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Report.pdf"'
    
    # Fetch data from the database and calculate values
    expenses = Expense.objects.filter(date__range=[start_date, end_date], user=request.user)
    incomes = Income.objects.filter(date__range=[start_date, end_date], user=request.user)
        
    user_profile = UserProfile.objects.get(user=request.user)
    total_income = sum(income.amount for income in incomes)
    total_expense = sum(expense.amount for expense in expenses)
    profit = total_income - total_expense

    # Calculate the value based on the formula provided
    if total_income + total_expense != 0:
        value = (total_income / (total_income + total_expense)) * 100
    else:
        value = -1
    
    
    Report.objects.create(
        user=request.user,
        username=user_profile.username,
        total_income=total_income,
        total_expense=total_expense,
        profit=profit
    )


    # Create a PDF document
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []  # Empty List 

   
    elements.append(Paragraph(f"Income & Expense Report of : {user_profile.username}", getSampleStyleSheet()['Heading1']))

   
    elements.append(Paragraph("<br/><br/><br/>Income Details :- ", getSampleStyleSheet()['Heading1']))

    # Prepare data for the income table
    income_data = [['No.', 'Source', 'Amount', 'Date', 'Category']]
    for idx, income in enumerate(incomes, start=1):
        income_data.append([idx, income.source, income.amount, income.date, income.category])

    # Create income table and style
    income_table = Table(income_data)
    income_style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gold),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.powderblue),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    income_table.setStyle(income_style)
    elements.append(income_table)

    elements.append(Paragraph("<br/><br/><br/>", getSampleStyleSheet()['Normal']))


    elements.append(Paragraph(f"Total Income:  {total_income}", getSampleStyleSheet()['Heading3']))

    elements.append(Paragraph("<br/><br/><br/>", getSampleStyleSheet()['Normal']))


    elements.append(Paragraph("Expense Details :- ", getSampleStyleSheet()['Heading1']))

    
    expense_data = [['No.', 'Name', 'Amount', 'Date', 'Category']]
    for idx, expense in enumerate(expenses, start=1):
        expense_data.append([idx, expense.name, expense.amount, expense.date, expense.category])

   
    expense_table = Table(expense_data)
    expense_style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gold),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.powderblue),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    expense_table.setStyle(expense_style)
    elements.append(expense_table)

    elements.append(Paragraph("<br/><br/><br/>", getSampleStyleSheet()['Normal']))

    # Add total expense and profit
    elements.append(Paragraph(f"Total Expense:  {total_expense}", getSampleStyleSheet()['Heading3']))

    elements.append(Paragraph("<br/><br/><br/><br/>", getSampleStyleSheet()['Normal']))
    if profit >= 0:
       elements.append(Paragraph(f"Profit:  {profit}", getSampleStyleSheet()['Heading2']))
    elif profit < 0:
       elements.append(Paragraph(f"Loss:  {profit}", getSampleStyleSheet()['Heading2']))
    elements.append(Paragraph("<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>", getSampleStyleSheet()['Normal']))

    elements.append(Paragraph(f"Your Status related to Income and Expense :- ", getSampleStyleSheet()['Heading1']))

    # Add image based on value condition
    if 0 <= value < 50:
        img_path = 'C:\\Users\\Rushang Gajera\\OneDrive\\Desktop\\wealthplus1\\static\\loss.jpg'
    elif 50 <= value < 60:
        img_path = 'C:\\Users\\Rushang Gajera\\OneDrive\\Desktop\\wealthplus1\\static\\expenses-income-balance-pictured-as-.webp' 
    elif 60 <= value < 90:
        img_path = 'C:\\Users\\Rushang Gajera\\OneDrive\\Desktop\\wealthplus1\\static\\high-income-and-low-expense-vector-3515202.jpg'
    elif 90 <= value <= 100:
        img_path = 'C:\\Users\\Rushang Gajera\\OneDrive\\Desktop\\wealthplus1\\static\\Income-PNG-Transparent-Image.png'  

    # Add the image to the PDF document
    if img_path:
        img = Image(img_path)
        img.drawHeight = 300  
        img.drawWidth = 300  
        elements.append(img)
    else:
        elements.append(Paragraph("Error: Report cannot be generated without income and expense data.", getSampleStyleSheet()['Normal']))

    # Build the PDF
    doc.build(elements)  # Download pdf.
    return response


def filter_report(request):
    if request.method == 'GET':
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
       
        if (not start_date) and (not end_date) :
            start_date = timezone.now().strftime('%Y-%m-%d')
            end_date = timezone.now().strftime('%Y-%m-%d')
        elif not start_date:
            start_date = end_date
        elif not end_date:
            end_date = start_date
        

        expenses = Expense.objects.filter(date__range=[start_date, end_date], user=request.user)
        incomes = Income.objects.filter(date__range=[start_date, end_date], user=request.user)
        
       
        total_incomes = sum(income.amount for income in incomes)
        total_expense = sum(expense.amount for expense in expenses)
        
       
        profit = total_incomes - total_expense
        
        if total_incomes + total_expense != 0:
            value = (total_incomes / (total_incomes + total_expense)) * 100
        else:
            value = -1
        
        #print(value)
        return render(request, 'report.html', {
            'incomes': incomes,
            'expenses': expenses,
            'total_incomes': total_incomes,
            'total_expense': total_expense,
            'profit': profit,
            'value': value,
            'user': request.user,
            'start_date' : start_date,
            'end_date' : end_date
          })
      
    else:
        return render(request, 'report.html')
        