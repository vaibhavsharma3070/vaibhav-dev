from django import forms 
from .models import AppData , CustomUser , userFiles
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.core.validators import validate_email
import re

  
  
# creating a form 
class ApplicationDataForm(forms.ModelForm): 
  
    # create meta class 
    class Meta: 
        # specify model to be used 
        model = AppData 
  
        # specify fields to be used 
        fields = [ 
            "KEY", 
            "VALUE", 
        ] 



class UserFilesForm(forms.ModelForm):
            doc = forms.FileField(label_suffix="",required=False,label="Resume",widget=forms.FileInput)
            img = forms.ImageField(label_suffix="",required=False,label="Image",widget=forms.FileInput) 
            
            class Meta:
                model = userFiles
                fields = [
                'doc','img',]
                
