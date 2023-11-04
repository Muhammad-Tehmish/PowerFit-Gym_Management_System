from django.shortcuts import render, redirect
from django.http import HttpResponse
import sqlite3
from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponseRedirect
from django import forms

# Connect to the SQLite database
conn = sqlite3.connect('/db.sqlite3')
conn.isolation_level = None  # Set auto-commit mode
cursor = conn.cursor()

# Create your views here.

def index(request):
    return render(request, 'index.html')

def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Connect to the SQLite database
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()

        # Check if the entered email and password match the records in MEMBER_LOGIN table
        cursor.execute("SELECT EMAIL, PASSWORD FROM MEMBER_LOGIN WHERE EMAIL = ? AND PASSWORD = ?;",(email, password))
        member = cursor.fetchall()
        conn.close()
        if member:
            # Redirect to member dashboard if credentials are correct
            return render(request,'member-dashboard.html')
        else:
            # Invalid credentials, show error message or redirect to login page with an error flag
            return render(request, 'signin.html', {'error': 'Invalid email or password'})
    
    return render(request, 'signin.html')  


def signup(request): 
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        plan = request.POST.get('plan')
        
        # Connect to the SQLite database
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor() 
        
        # Select from the member into the MEMBERSHIP_PLAN table
        cursor.execute("SELECT MEMBERSHIP_PLAN_ID FROM MEMBERSHIP_PLAN WHERE MEMBERSHIP_NAME = ?;", (plan,))
        query = cursor.fetchall()
   
        # Retrieve the maximum existing member ID from the table
        cursor.execute("SELECT MAX(MEMBER_ID) FROM MEMBERS;")
        result = cursor.fetchone()
        last_member_id = result[0] if result[0] else 0
        
        # Increment the last member ID to generate a new ID
        new_member_id = last_member_id + 1
        
        # Insert the signup information into the MEMBERS table
        cursor.execute("INSERT INTO MEMBERS (MEMBER_ID, NAME, EMAIL, PASSWORD, MEMBER_PLAN) VALUES (?, ?, ?, ?, ?);", (new_member_id, name, email, password, query[0][0]))
        conn.commit()
        
        # Insert the login credentials into the MEMBER_LOGIN table
        cursor.execute("INSERT INTO MEMBER_LOGIN (EMAIL, PASSWORD) VALUES (?, ?);", (email, password))
        conn.commit()

        print("Received data - Name: {}, Email: {}, Password: {}, Plan: {}".format(name, email, password, plan))

        
        conn.close()
        
        # Redirect to the member dashboard page
        return render(request, 'member-dashboard.html')
    
    else:
        return render(request, 'signin.html')



def adminlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Connect to the SQLite database
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()

        # Check if the entered email and password match the records in MEMBER_LOGIN table
        cursor.execute("SELECT EMAIL, PASSWORD FROM GYM_ADMIN WHERE EMAIL = ? AND PASSWORD = ?;",(email, password))
        member = cursor.fetchall()
        print(member)
        conn.close()
        if member:
            # Redirect to member dashboard if credentials are correct
            return render(request,'admin-dashboard.html')
        else:
            # Invalid credentials, show error message or redirect to login page with an error flag
            return render(request, 'gym-admin-login.html', {'error': 'Invalid email or password'})
    
    return render(request, 'gym-admin-login.html',)
    
def admindashboard(request):
    return render(request, 'admin-dashboard.html')

def admindashboardmembers(request):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    if request.method == 'GET':
       cur.execute('SELECT * FROM MEMBERS;')
       rows = cur.fetchall()
    else:
        name = request.POST.get('search')   
        cur.execute('SELECT * FROM MEMBERS WHERE NAME = ?;',(name,))
        rows = cur.fetchall()
    data = {'cat': rows}    
    conn.close()
    return render(request, 'admin-dashboard-members.html', data)

def admindashboardtrainers(request):
    if request.method == 'GET':
      conn = sqlite3.connect('db.sqlite3')
      cur = conn.cursor()
      cur.execute('SELECT * FROM TRAINERS;')
      rows = cur.fetchall()
      data = {'cat':rows}
      conn.close()
    return render(request, 'admin-dashboard-trainers.html', data)

def admindashboardequipment(request):
    return render(request, 'admin-dashboard-equipment.html')

def admindashboardplans(request):
    if request.method == 'GET':
      conn = sqlite3.connect('db.sqlite3')
      cur = conn.cursor()
      cur.execute('SELECT * FROM MEMBERSHIP_PLAN;')
      rows = cur.fetchall()
      data = {'cat':rows}
      return render(request, 'admin-dashboard-plans.html', data)

def memberdashboard(request):
    return render(request, 'member-dashboard.html')

def memberdashboardschedule(request):
    if request.method == 'GET':
     conn = sqlite3.connect('db.sqlite3')
     cur = conn.cursor()
     cur.execute('SELECT CLASS_NAME, CLASS_DAY, CLASS_TIME FROM CLASSES;')
     rows = cur.fetchall()
     data = {'cat':rows}
     conn.close()
     return render(request, 'member-dashboard-schedule.html', data)

def memberdashboardfee(request):
    return render(request, 'member-dashboard-fee.html')

def delete_mem(request, id):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    if request.method == 'POST':
        cur.execute("DELETE FROM MEMBERS WHERE MEMBER_ID = ?;",(id,))
        conn.commit()
        return HttpResponseRedirect("/admin-dashboard-members")
    conn.close()

def addtrainer(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        
        # Connect to the SQLite database
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()

        # Insert the add information into the TRAINERS table
        cursor.execute("INSERT INTO TRAINERS (NAME, EMAIL, PHONE) VALUES (?, ?, ?);", (name, email, phone))
        conn.commit()
        conn.close()
        return HttpResponseRedirect('/admin-dashboard-trainers')
    
    else:
        return render(request, 'add-trainer.html')

def delete_train(request, id):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    if request.method == 'POST':
        cur.execute("DELETE FROM TRAINERS WHERE TRAINER_ID = ?;",(id,))
        conn.commit()
        return HttpResponseRedirect("/admin-dashboard-trainers")
    conn.close()  

def update_plan(request, name):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    
    class Plan_update_Form(forms.Form):
        Price = forms.CharField(label='Price', widget=forms.TextInput(attrs={'class':'form-control'}))
    if request.method == "POST":
        price = request.POST.get('Price')
        cur.execute("UPDATE MEMBERSHIP_PLAN SET PRICE = ? WHERE MEMBERSHIP_NAME = ?;", (price, name))
        conn.commit()
        conn.close()
        return HttpResponseRedirect('/admin-dashboard-plans')
    conn.close()
    fm = Plan_update_Form()
    return render(request, 'update-plan.html', {'form_upd':fm})   

