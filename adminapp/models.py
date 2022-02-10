from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save,pre_delete
from django.dispatch import receiver
from mainapp.models import CustomUser




#Projects data models.
class Projects(models.Model): 
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    project_url = models.CharField(max_length=100,default="")
    owner = models.ForeignKey(CustomUser, default=1, verbose_name="Owner", on_delete=models.SET_DEFAULT)
    estimated_time =models.CharField(max_length = 100,default="")
    budget = models.DecimalField(max_digits=19, decimal_places=2,default="0.0")
    short_description =models.TextField(default="") 
    description=models.TextField(default="")
    state  = models.CharField(max_length = 100,default="In-progress") #Radio Button Waiting, canceled,In-progress,Completed
    similar_project = models.CharField(max_length=150,default="") 
    project_description = models.FileField()
    tags_of_used_technology =models.CharField(max_length = 150,default="")
    main_major  = models.CharField(max_length = 200,default="")
    progress =models.IntegerField(default=0)
    created	= models.DateTimeField(verbose_name='Created', auto_now_add=True)
    release_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, default="",related_name="project_created_by", on_delete=models.SET_DEFAULT) 
    

    def __str__(self):
        return self.name
    
    

    

#Assignees data models.
class Assignees(models.Model): 
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100)
    assigned_person = models.ForeignKey(CustomUser, default=1, related_name="assigneed_person", on_delete=models.SET_DEFAULT)
    project =  models.ForeignKey(Projects, default=1, related_name="project_assignee", on_delete=models.CASCADE)
    created	= models.DateTimeField(verbose_name='Created', auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, default="",related_name="project_assignee_created", on_delete=models.SET_DEFAULT)   
    def __str__(self):
        return self.id

#Response data models.
class Responses(models.Model): 
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100,default="response")
    response = models.TextField(default="")
    project =  models.ForeignKey(Projects, default="", related_name="Project_response", on_delete=models.CASCADE)  
    created	= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, default="",related_name="project_response_created", on_delete=models.SET_DEFAULT)
     
    def __str__(self):
        return self.id

#Response data models.
class ProjectFilesAndImages(models.Model): 
    id = models.AutoField(primary_key=True)
    file = models.FileField()
    type = models.CharField(max_length=100,default="image")
    subtype = models.CharField(max_length=100,default="secondary")
    project =  models.ForeignKey(Projects, default="", related_name="Project_file", on_delete=models.CASCADE)
    created	= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, default="",related_name="project_file_created", on_delete=models.SET_DEFAULT)   
    def __str__(self):
        return self.id
    def save(self, *args, **kwargs): #prewrite
        # if image type is primary update existing images to secondary
        print("test",self.project.id)
        if self.subtype == "primary" :
            print("test",self.project.id)
            primary_image = ProjectFilesAndImages.objects.filter(project=self.project.id,subtype="primary")
            if primary_image.count() > 0 :
                print("test",primary_image.count())
                ProjectFilesAndImages.objects.filter(project=self.project.id,type="image").update(subtype='secondary')
                pass            
        else:
            # If primary image does not exist make secondary to primary
            primary_image = ProjectFilesAndImages.objects.filter(project=self.project.id,subtype="primary")
            if len(primary_image) > 0 :
                 #Primary image exist 
                 pass
            else:
                 self.subtype="primary"
        super(ProjectFilesAndImages, self).save(*args, **kwargs) 


# pre_delete _project - Delete files,responses and assignees before delting project
def deletes_files_responses_assignees(sender, instance, **kwargs): 
    project_id = instance.id
    ProjectFilesAndImages.objects.filter(project=project_id).delete()
    Responses.objects.filter(project=project_id).delete()
    Assignees.objects.filter(project=project_id).delete()

pre_delete.connect(deletes_files_responses_assignees, sender=Projects)

class Leads(models.Model): #Contact Us Model
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)        
    similar_project = models.CharField(max_length=150,default="") 
    project_description = models.FileField()    
    main_major  = models.CharField(max_length = 200,default="")    
    created	= models.DateTimeField(verbose_name='Created', auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, default="",related_name="lead_created_by", on_delete=models.SET_DEFAULT) 
    state  = models.CharField(max_length = 100,default="In-progress") #Radio Button Waiting, canceled,In-progress,Completed
    def __str__(self):
        return self.name

class LeadFilesAndImages(models.Model): #Contact Us Files and Images
        lead = models.OneToOneField(Leads, on_delete=models.CASCADE,related_name='Lead_file',default="1")
        doc = models.FileField(default="")
        img = models.ImageField(default="")


class Button(models.Model):
    name = models.CharField(max_length=100)
    page_title = models.CharField(max_length=100)
    url = models.CharField(max_length=100, null=True, blank=True)
    isAvailable_indicator = models.BooleanField()
    isSlider_available = models.BooleanField()
    isNew_flag = models.BooleanField()

class language(models.Model):
    language = models.CharField(max_length=100)
    language_code = models.CharField(max_length=100)
    def __str__(self):
        return self.language

class color(models.Model):
    color = models.CharField(max_length=100)
    def __str__(self):
        return self.color

class Slider(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    button_obj = models.ForeignKey(Button, on_delete=models.CASCADE,related_name='button_obj')
    def __str__(self):
        return self.title
        
