from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import AppData ,CustomUser
from django.contrib import messages 
from django.contrib.auth import authenticate
from django.contrib import auth
from adminapp.models import Projects
import math
from django.urls import reverse
from adminapp.models import *


# Create your views here.
def register(request):  
    if "female"  in request.POST:
        gender = 'F'
    else:
        gender = 'M'      
    born_at_day= request.POST['born_at_day']
    born_at_month = request.POST['born_at_month']
    born_at_year= request.POST['born_at_year']
    try:
        form = CustomUser.objects.create_user(name=request.POST['name'],email =request.POST['email'],phone= request.POST['phone'],
                            gender=gender,birthday=born_at_year+"-"+born_at_month+"-"+ born_at_day,password = request.POST['password1'] )  
        form.save()
    except Exception as e:
        messages.error(request,  e)
        return render(request, "mainapp/signup.html",{"name":request.POST['name'],"email":request.POST['email'],"phone":request.POST['phone']})

    return HttpResponseRedirect(reverse('login'))
    

def homepage(request):
    WHOSUS_Value =""
    WHYUS_Value = ""
    WHOSUS = AppData.objects.filter(KEY="WHOSUS")
    WHYUS = AppData.objects.filter(KEY="WHYUS")        
    if WHOSUS.exists() :
        print(WHOSUS)
        WHOSUS_Value =  WHOSUS[0].VALUE
    if WHYUS.exists() :
        WHYUS_Value =  WHYUS[0].VALUE  
    users = CustomUser.objects.filter(is_superuser=False, state='R')
    projects = Projects.objects.filter(state="Completed")
    buttons = Button.objects.all()
    # devide button into 5 dictionaries
    ###################################################################
    ###################################################################
    languages = language.objects.all()
    colors = color.objects.all()
    project_count = projects.count()
    external_loop = math.ceil(project_count / 5)
    d = {
    "WHOSUS":WHOSUS_Value,
    "WHYUS":WHYUS_Value,
    "users":users,
    "projects":projects,
    "external_loop":range(external_loop),
    "internal_loop":range(5), 
    "buttons":buttons, 
    "languages":languages, 
    "colors":colors,
        "butt": get_footer_data(),
    }        
    return render(request, "mainapp/index.html",d)



def login(request):
    if request.method == 'POST':
        login = request.POST['login']
        pwd = request.POST['password']
        user = authenticate(email = request.POST['login'],password=request.POST['password'])        
        if user is not None :
            if user.is_admin:
                response = redirect(reverse('home_page')) #admin will go to homepage
            else:
                response = redirect(reverse('projects',kwargs={'page':'assigned'})) #non-admin user will go to assigned project
            if user.is_active :
                request.user=user
                auth.login(request, user)
                if request.POST['RememberMe'] :
                     response.set_cookie('email', login)  #cookies set
                return response
            else:
                messages.error(request,  "User is not active.")
                return render(request, "mainapp/login.html")
        else:
            messages.error(request,  "Incorrect login password.")
            return render(request, "mainapp/login.html", {"butt": get_footer_data(), "buttons": Button.objects.all()})
        
    else:
        if request.user.is_authenticated:
            return redirect("/EmployeeFacing")
        else:
            return render(request, "mainapp/login.html", {"butt": get_footer_data(), "buttons": Button.objects.all()})


def signup(request):
    return render(request, "mainapp/signup.html", {"butt": get_footer_data(), "buttons": Button.objects.all()})


def get_footer_data():
    buttons = Button.objects.all()
    butt = []
    count = 1
    but = {}
    for data in buttons:
        print(count)
        if count == 1:
            if 'value' in but:
                but['value'].append(data)
            else:
                but['value'] = [data]
            count = count + 1
        elif count <= 6:
            if 'value' in but:
                but['value'].append(data)
            else:
                but['value'] = [data]
            count = count + 1
        elif count > 6:
            count = 1
            butt.append(but)
            but = {}
            if 'value' in but:
                but['value'].append(data)
            else:
                but['value'] = [data]
    if but:
        butt.append(but)
    return butt
