'''
Description : This form is used to add new user.
              validations and clean data is according to add user
'''
from django import forms 
from .models import AppData , CustomUser , userFiles
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.core.validators import validate_email
import re

COUNTRIES = [('IN','INDIA'),
         ('UK','UK'),
         ('US','US'),]

STATE_CHOICES=[('P','Pending'),
         ('R','Ready')]
GENDER_CHOICES=[('M','Male'),
         ('F','Female')]
         

COUNTRIES = [('IN','INDIA'),
         ('UK','UK'),
         ('US','US'),]

STATE_CHOICES=[('P','Pending'),
         ('R','Ready')]
GENDER_CHOICES=[('M','Male'),
         ('F','Female')]
         
USER_TYPE = [('Admin','Admin'),
              ('Team Member','Team Member'),]  
class UserForm(UserCreationForm): 
            type = forms.ChoiceField(required=False,choices=USER_TYPE,label_suffix="", widget=forms.Select(attrs={'class':'form-control'}))           
            email = forms.EmailField(required=False,label_suffix="",max_length=100,widget= forms.TextInput(attrs={'class':'form-control','autofocus': False}))
            name  = forms.CharField(required=False,label_suffix="",max_length=100,widget= forms.TextInput(attrs={'class':'form-control','autofocus': True}))
            spacialist  = forms.CharField(required=False,label_suffix="",max_length=100,widget= forms.TextInput(attrs={'class':'form-control'}))
            currentwork  = forms.CharField(required=False,label_suffix="",max_length=100,widget= forms.TextInput(attrs={'class':'form-control'}))
            company  = forms.CharField(required=False,label_suffix="",max_length=100,widget= forms.TextInput(attrs={'class':'form-control'}))
            phone  = forms.CharField(required=False,label_suffix="",max_length=100,widget= forms.TextInput(attrs={'class':'custom-form-control phone'}))
            Country  = forms.ChoiceField(required=False,choices=COUNTRIES,label_suffix="", widget=forms.Select(attrs={'class':'custom-form-control country'}))
            state = forms.ChoiceField(required=False,label_suffix="",label='State',choices=STATE_CHOICES, widget=forms.RadioSelect(attrs={'display': 'inline-block'}))
            gender = forms.ChoiceField(required=False,label_suffix="",label='Gender',choices=GENDER_CHOICES, widget=forms.RadioSelect(attrs={'display': 'inline-block'}))
            birthday =  forms.DateField(required=False,label_suffix="",widget=forms.DateInput(attrs={'class':'datepicker form-control'},format='%m/%d/%Y'))
            tags_of_used_technology= forms.CharField(required=False,label_suffix="",max_length=100,widget= forms.TextInput(attrs={'class':'form-control'}))
            short_description = forms.CharField(required=False,label_suffix="",widget= forms.Textarea(attrs={'class':'form-control'}))
            password1  = forms.CharField(required=False,label='Password', label_suffix="",max_length=100,widget= forms.PasswordInput(attrs={'class':'form-control'}))
            password2  = forms.CharField(required=False,label='Confirm Password',label_suffix="",max_length=100,widget= forms.PasswordInput(attrs={'class':'form-control'}))

            class Meta:
                model = CustomUser
                fields =  [
                'email','name', 'spacialist','currentwork','company', 'phone','Country','state', 'gender','birthday', 'tags_of_used_technology',
                 'short_description']
            #Validation for phone Field
            def clean_phone(self):
                    print(self.cleaned_data.get("phone"))
                    regex=re.compile('\(?\+[0-9]{1,3}\)? ?-?[0-9]{1,3} ?-?[0-9]{3,5} ?-?[0-9]{4}( ?-?[0-9]{3})? ?(\w{1,10}\s?\d{1,6})?', re.I)
                    print(bool(regex.match(str(self.cleaned_data.get("phone")))))
                    cleaned_data = self.cleaned_data                    
                    if not bool(regex.match(str(self.cleaned_data.get("phone")))):
                                    raise forms.ValidationError("Phone number must be entered in the format: '+59 12345678'.")
                    return cleaned_data['phone']

            #Validation for email Field
            def clean_email(self):
                    cleaned_data = self.cleaned_data
                    print(cleaned_data.get("email"))
                    if  validate_email(cleaned_data.get("email")):
                                    raise forms.ValidationError("email is required")
                    return cleaned_data['email']

            #Validation for company Field
            def clean_company(self):
                    cleaned_data = self.cleaned_data
                    print(cleaned_data.get("company"))
                    if not cleaned_data.get("company"):
                                    raise forms.ValidationError("company is required")
                    return cleaned_data['company']

            #Validation for currentwork Field
            def clean_currentwork(self):
                    cleaned_data = self.cleaned_data
                    print(cleaned_data.get("currentwork"))
                    if not cleaned_data.get("currentwork"):
                                    raise forms.ValidationError("currentwork is required")
                    return cleaned_data['currentwork']

            #Validation for spacialist Field
            def clean_spacialist(self):
                    cleaned_data = self.cleaned_data
                    print(cleaned_data.get("spacialist"))
                    if not cleaned_data.get("spacialist"):
                                    raise forms.ValidationError("spacialist is required")
                    return cleaned_data['spacialist']

            #Validation for name Field
            def clean_name(self):
                    cleaned_data = self.cleaned_data
                    print(cleaned_data.get("name"))
                    if not cleaned_data.get("name"):
                                    raise forms.ValidationError("name is required")
                    return cleaned_data['name']

            #Validation for short_description Field
            def clean_short_description(self):
                    cleaned_data = self.cleaned_data
                    print(cleaned_data.get("short_description"))
                    if not cleaned_data.get("short_description"):
                                    raise forms.ValidationError("Short Description is required")
                    return cleaned_data['short_description']
                    
            #Validation for short_description Field
            def clean_tags_of_used_technology(self):
                    cleaned_data = self.cleaned_data
                    print(cleaned_data.get("tags_of_used_technology"))
                    if not cleaned_data.get("tags_of_used_technology"):
                                    raise forms.ValidationError("tags_of_used_technology is required")
                    return cleaned_data['tags_of_used_technology']