from django import forms 
from .models import Leads,LeadFilesAndImages
from django.conf import settings


class contact_us_form(forms.ModelForm): #form for contact us
            required_css_class = 'required'
            name  = forms.CharField(label='Project Title',required=True,label_suffix="",max_length=100,widget= forms.TextInput(attrs={'class':'form-control'}))
            similar_project = forms.CharField(label='Similar Project (if any)',
                                              required=False,label_suffix="",
                                              max_length=150,
                                              widget= forms.TextInput(attrs={'class':'form-control'}))
            project_description  = forms.CharField(required=True,label='Description of the project',
                                        label_suffix="",
                                        widget= forms.Textarea(attrs={'class':'form-control','rows':'5'})
                                        )
            main_major  = forms.CharField(required=True,label_suffix="",label='Project Main Major',max_length=200,widget= forms.TextInput(attrs={'class':'form-control'}))
            class Meta:
                model = Leads
                fields = ['name','similar_project',
                'project_description','main_major',]

class contact_us_form_files(forms.ModelForm): #form for contact us
            doc = forms.FileField(label_suffix="",required=False,label="Have file with all details",widget=forms.FileInput(attrs={'class':'form-control'}))
            img = forms.ImageField(label_suffix="",required=False,label="Image of the project",widget=forms.FileInput(attrs={'class':'form-control'}))
            class Meta:
                model = LeadFilesAndImages
                fields = [
                'doc','img',]