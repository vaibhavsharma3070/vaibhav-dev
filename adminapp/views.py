from django.shortcuts import render, redirect
from django.http import HttpResponse
from mainapp.models import AppData,CustomUser,userFiles
from adminapp.models import Button, Projects,Responses,ProjectFilesAndImages,Assignees,Leads, Slider
from adminapp.add_project_form import add_project_form
from django.http import JsonResponse
from mainapp.forms import ApplicationDataForm,UserFilesForm # application data form
from mainapp.edit_user_form import UserUpdateForm,UserUpdateFormNonAdmin  #User update Form
from adminapp.contact_us_form import contact_us_form ,contact_us_form_files  #contact us related form
from mainapp.add_user_form import UserForm  #User add form
from adminapp.add_project_response_form import ProjectResponseForm  #User add form
from django.contrib import messages 
from adminapp.image_upload_form import ProjectFilesAndImagesForm
from django.db.models import Q
import math
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views.generic.edit import FormView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy,reverse
from django.conf import settings  #NUM_OF_RECORD_IN_LIST_VIEW



#contact_us
def contact_us(request):
    # Contact us view is for contact us form.
    if request.method == 'POST': #click save button on Contact Us
        lead = contact_us_form(request.POST,request.FILES) #Get lead details
        files = contact_us_form_files(request.POST, request.FILES)  #Get File Related data from FORM  
        if lead.is_valid() and files.is_valid():            
            lead_form = lead.save(commit=False)
            lead_form.created_by_id =  request.user.id         
            lead_form.save()             
            lead_files = files.save(commit=False)  
            lead_files.lead_id = lead_form.id           
            if 'doc' in  request.FILES.keys():                    
                    lead_files.doc = request.FILES['doc']
            if 'img' in  request.FILES.keys():                    
                    lead_files.img = request.FILES['img']                      
            lead_files.save()
            return redirect(contact_us)
        else:
            all_leads = Leads.objects.filter(created_by=request.user.id)
            context={"lead_form":lead,"lead_files":files,"all_leads":all_leads}
            return render(request, "adminapp/contact_us.html",context)                     
    else:
        lead_form= contact_us_form()
        lead_files= contact_us_form_files()
        if request.user.is_admin :
            #Admin user would be able to see all 
            all_leads = Leads.objects.all()
        else:
            all_leads = Leads.objects.filter(created_by=request.user.id)
        context={"lead_form":lead_form,"lead_files":lead_files,"all_leads":all_leads}
        return render(request, "adminapp/contact_us.html",context)

#team_project_detail
class team_project_detail(LoginRequiredMixin, TemplateView):
    '''
    Detail : This class has been used to display project in detail
    URL :teamprojectdetail/<str:id>   
    '''
    template_name = 'adminapp/team_project_detail.html'  
    def get_context_data(self, *args, **kwargs):
            context = super().get_context_data(*args, **kwargs)
            id=kwargs['id']
            project =  Projects.objects.get(id=id) #Search Record
            projrct_file = ProjectFilesAndImages.objects.filter(project=id).order_by('-id') #ProjectImages            
            assignees = Assignees.objects.filter(project=id)  
            context['responses'] =  Responses.objects.filter(project=id).order_by('-created')
            context['project'] = project
            context['projrct_file'] = projrct_file
            context['assignees'] = assignees
            return context

class complete_project_detail(TemplateView):
    '''
    Detail : This class has been used to display project in detail
    URL :ourwork/<str:id>   
    '''
    template_name = 'adminapp/complete_project_detail.html'  
    def get_context_data(self, *args, **kwargs):
            context = super().get_context_data(*args, **kwargs)
            id=kwargs['id']
            project =  Projects.objects.get(id=id) #Search Record  
            projrct_file = ProjectFilesAndImages.objects.filter(project=id).order_by('-id') #ProjectImages                     
            assignees = Assignees.objects.filter(project=id)             
            context['project'] = project            
            context['assignees'] = assignees
            context['projrct_file'] = projrct_file
            return context

#Add Project
class  add_project(LoginRequiredMixin,UserPassesTestMixin, CreateView):
        '''
        Detail : This class has been used to add project detail from admin panel.
        URL : /addproject/
        form : mainapp.add_user_form
        '''
        template_name = 'adminapp/add_project.html'
        form_class = add_project_form        

        def test_func(self):
            return self.request.user.is_admin == True

        def get_initial(self, *args, **kwargs):
            initial = super().get_initial(**kwargs)
            initial['state'] = 'In-progress'
            return initial
        
        def form_valid(self, form):
            self.object = form.save(commit=False)
            self.object.created_by = self.request.user
            self.object.save()
            
            return HttpResponseRedirect(self.get_success_url())

        def get_success_url(self):
            success_url = reverse_lazy('edit_project', kwargs={'id': self.object.pk})            
            return success_url
            

#Add User
def add_user(request):
    '''
    Detail : This function has been used to add user detail from admin panel.
    URL : /adduser/
    form : mainapp.add_user_form
    '''
    if request.method == 'POST':
        user = UserForm(request.POST,request.FILES) #Get user related detail from FORM
        files = UserFilesForm(request.POST, request.FILES)  #Get File Related data from FORM  
        if user.is_valid() and files.is_valid():            
            userForm = user.save(commit=False)           
            userForm.save()             
            userFileForm = files.save(commit=False)  
            userFileForm.user_id = userForm.id           
            if 'doc' in  request.FILES.keys():                    
                    userFileForm.doc = request.FILES['doc']
            if 'img' in  request.FILES.keys():                    
                    userFileForm.img = request.FILES['img']                      
            userFileForm.save()            
            users =  CustomUser.objects.all()
            return render(request, "adminapp/users.html",{"users":users})
        else:
            return render(request, "adminapp/add_user.html",{"userForm":user,"userFileForm":files})
    else:
        userForm = UserForm() #Create User Form with password
        userFileForm = UserFilesForm()  
        return render(request, "adminapp/add_user.html",{"userForm":userForm,"userFileForm":userFileForm}) #Redirect to add_user 

#user_profile
def user_profile(request,email):
    '''
    Detail : This function has been used for user profile.
    URL : /userprofile/<str:email>/
    '''
    record =  CustomUser.objects.get(email=email) #Search Record
    involved = Assignees.objects.filter(assigned_person=record.id)
    projects = Projects.objects.filter(Q(project_assignee__in=involved),state="Completed")
    project_count = projects.count()
    external_loop = math.ceil(project_count / 5)
    try:
            FileRecord =userFiles.objects.get(user_id=record.id) #Serch record in File Table
    except :
            FileRecord = None
    context ={"record":record,"FileRecord":FileRecord,"projects":projects,"external_loop":range(external_loop),"internal_loop":range(5)}
    return render(request, "adminapp/user_profile.html",context)

# Edit User
def edit_user(request,email):
    '''
    Detail : This function has been used to update user detail from admin panel.
    URL : /edituser/<str:email>/
    '''
    record =  CustomUser.objects.get(email=email) #Search Record
    try:
            FileRecord =userFiles.objects.get(user_id=record.id) #Serch record in File Table
    except :
            FileRecord = None
    if request.method == 'POST':
        if request.user.is_admin:
            user = UserUpdateForm(request.POST,request.FILES,instance=record) #Get duser related detail from FORM
        else:
            user = UserUpdateFormNonAdmin(request.POST,request.FILES,instance=record) #Get duser related detail from FORM
        files = UserFilesForm(request.POST, request.FILES,instance=FileRecord)  #Get File Related data from FORM    
        if user.is_valid() and files.is_valid():            
            userForm = user.save(commit=False)
            userForm.save()             
            userFileForm = files.save(commit=False) 
                    
            if 'doc' in  request.FILES.keys():
                    if FileRecord.doc !="" :
                        try:
                            old_file = userFiles.objects.get(user_id=record.id).doc
                            old_file.delete(save=True) #Delete the previous files before upload
                        except :
                           pass                
                    userFileForm.doc = request.FILES['doc']
                   
            if 'img' in  request.FILES.keys():
                    try:
                        old_file = userFiles.objects.get(user_id=record.id).img
                        old_file.delete(save=True) #Delete the previous files before upload
                    except :
                           pass
                    userFileForm.img = request.FILES['img'] 
                     
                              
            userFileForm.save()             
            users =  CustomUser.objects.all()
            return redirect(user_profile,userForm.email)
        else:
            
            return render(request, "adminapp/edit_user.html",{"userForm":user,"userFileForm":files})
        
    else:
        #if it is not a POST Request 
        if request.user.is_admin:      
            userForm = UserUpdateForm(instance=record)
        else:
            userForm = UserUpdateFormNonAdmin(instance=record)
        userFileForm = UserFilesForm(instance=FileRecord)      
        if record:                              
                return render(request, "adminapp/edit_user.html",{"userForm":userForm,"userFileForm":userFileForm})
        else:
            users =  CustomUser.objects.all()
            return render(request, "adminapp/users.html",{"users":users})




def edit_project(request,id):
    '''
    Detail : This function has been used to edit project
    URL : /editproject/<str:id>    
    '''
    project = Projects.objects.get(id=id) #query a projects
    if request.method == 'POST':
        assignees = request.POST["assignees"]        
        project_form = add_project_form(request.POST,instance=project)
        if project_form.is_valid():            
            project = project_form.save(commit=False)
            project.save()
            # remove previous assignees
            Assignees.objects.filter(project=id).delete()
            # add assignees
            for i in assignees.split(','): 
                        if i !="" :
                            assigned_person_object = CustomUser.objects.get(id=i)
                            Assignees.objects.create(project=project,assigned_person=assigned_person_object,type="Assignee",created_by=request.user); 
            return redirect(reverse('team_project_detail', kwargs={'id':id}))
        else:
           return render(request, "adminapp/edit_project.html",{"project_form":project_form}) 
        
    else:        
        project_form = add_project_form(instance=project)
        users_for_assignmnets = CustomUser.objects.filter(is_superuser=False)
        assignees = Assignees.objects.filter(project=id)  
        context = {"project_form":project_form,"users_for_assignmnets":users_for_assignmnets,"assignees":assignees}
        return render(request, "adminapp/edit_project.html",context)

class project(LoginRequiredMixin, TemplateView):
    '''
    Detail : This class has been used to display projects to user
    URL : /project/assigned
        : /project/queued
    '''
    template_name = 'adminapp/project_queue.html'  
    def get_context_data(self, *args, **kwargs):
          context = super(project, self).get_context_data(*args, **kwargs)
          page=kwargs['page']
          if page == "assigned" : 
            # URL :/project/assigned        
            involved = Assignees.objects.filter(assigned_person=self.request.user.id)
            projects = Projects.objects.filter(Q(project_assignee__in=involved)) #query user specific projects 
          elif page == "queued" :
            # URL :/project/queued
            if self.request.user.is_admin:
                projects = Projects.objects.all() #query all projects for project queue page
            else:
               raise PermissionDenied()
          context['projects'] = projects
          return context

class user(LoginRequiredMixin,UserPassesTestMixin, ListView):
        '''
        Detail : This class has been used to display all users
        URL : /users        
        '''
        template_name = 'adminapp/users.html'
        paginate_by = settings.NUM_OF_RECORD_IN_LIST_VIEW
        model = CustomUser
        context_object_name = 'users'
        queryset = CustomUser.objects.filter(is_superuser=False) 

        def test_func(self):
            return self.request.user.is_admin == True

class home_page(LoginRequiredMixin,UserPassesTestMixin, ListView):
        '''
        Detail : This class has been used to display home page of logged in user
        URL : /users        
        '''
        template_name = 'adminapp/homepage.html'
        paginate_by = settings.NUM_OF_RECORD_IN_LIST_VIEW
        model = Projects
        context_object_name = 'projects'
        queryset = Projects.objects.all()
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            WHOSUS = AppData.objects.filter(KEY="WHOSUS")
            WHYUS = AppData.objects.filter(KEY="WHYUS")
            if WHOSUS.exists() :       
                WHOSUS_Value =  WHOSUS[0].VALUE
            else:
                WHOSUS_Value = "" # if record not exist

            if WHYUS.exists() :
                WHYUS_Value =  WHYUS[0].VALUE 
            else:
                WHYUS_Value = "" # if record not exist   
            context['WHOSUS'] = WHOSUS_Value
            context['WHYUS'] = WHYUS_Value
            context['buttons'] = Button.objects.all()
            context['butt'] = get_footer_data()
            return context

        def test_func(self):
            return self.request.user.is_admin == True


def ApplicationDataUpdate(request):
        '''
        Description : This method is for all AJAX responses.
        '''
        if request.method == 'POST':
            if request.POST['AREA'] == 'RESPONSE': #Insert Response
                form = ProjectResponseForm(request.POST)
                if form.is_valid() :
                     form.save()
                else:
                   print(form.errors)
                data = {'output': form.errors }
                return JsonResponse(data)

            if request.POST['AREA'] == 'LOV':                
                KEY = request.POST['KEY']
                VALUE = request.POST['VALUE']
                record = AppData.objects.filter(KEY=KEY)
                if record.exists():
                    record[0].VALUE=VALUE
                    form = ApplicationDataForm(request.POST or None, instance = record[0]) 
                    if form.is_valid() :                              
                        form.save()
                else:
                    newRecord = AppData(KEY=KEY,VALUE = VALUE) 
                    newRecord .save() 
                data = {'output': 'Successful' }           
                return JsonResponse(data)

            if  request.POST['AREA'] == 'USERDISABLE':
                # AjaxCall(email,'Disable','USERDISABLE','{{ csrf_token }}'); 
                record = CustomUser.objects.filter(email=request.POST['KEY'])
                if record.exists(): 
                    user =  record[0]
                    if request.POST['VALUE'] =="Disable" : 
                        user.is_active = False
                        user.save()
                        data = {'output': 'Profile successfully disabled.' }           
                        
                    else:
                        user.is_active = True
                        user.save()
                        data = {'output': 'Profile successfully enabled.' }
               
                return JsonResponse(data)
            
            if  request.POST['AREA'] == 'ProjectImageUpload':
                # Project Image upload
                form = ProjectFilesAndImagesForm(request.POST,request.FILES)
                if form.is_valid() :
                     f = form.save(commit=False)
                     f.created_by = request.user
                     f.save()
                else:
                    print(form.errors)
                data = {'output': 'Profile successfully enabled.' }
                return JsonResponse(data)

def not_found(request):
    projects = Projects.objects.filter(state="Completed")
    buttons = Button.objects.all()

    ###################################################################
    context = {"projects":projects,"buttons":buttons, "butt":get_footer_data()}
    return render(request, 'adminapp/404.html', context)


def product(request, id):
    '''
    Detail : This class has been used to display product details
    URL : /product/<id>
    '''
    product = Button.objects.get(id=id)
    if product.isSlider_available:
        
        # get 1st slide
        try:
            slider_1 = Slider.objects.filter(button_obj__id=id).order_by('-id')[0]
            sliders = Slider.objects.filter(button_obj__id=id).order_by('-id')[0:]
        except:
            return redirect('not_found')
        projects = Projects.objects.filter(state="Completed")
        # for data in butt:
        #     print(data['title'])
        #     for d in data['value']:
        #         print(d.name)
        buttons = Button.objects.all()
        context = {"projects":projects,"buttons":buttons, "slider_1":slider_1, "sliders":sliders, product:product, "butt":get_footer_data()}
        return render(request, 'adminapp/product_detail.html', context)
    elif product.isAvailable_indicator:
        url = product.url
        return redirect(url)
    else:
        return redirect('not_found')



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
