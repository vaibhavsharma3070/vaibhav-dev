from django import forms 
from .models import Projects   #project model
from django.conf import settings
from mainapp.models import CustomUser # All users

STATE_CHOICES=[('Completed','Completed'),('In-progress','In-progress'),('Waiting','Waiting'),('Canceled','Canceled'),]

class add_project_form(forms.ModelForm):
            name  = forms.CharField(label='Project Title',required=False,label_suffix="",max_length=100,widget= forms.TextInput(attrs={'class':'form-control'}))
            owner  =forms.ModelChoiceField(label='Project Owner',required=False,queryset=CustomUser.objects.filter(is_superuser=False),label_suffix="",widget= forms.Select(attrs={'class':'form-control'}))
            estimated_time = forms.CharField(required=False,label_suffix="",max_length=200,widget= forms.TextInput(attrs={'class':'form-control'}))
            budget = forms.DecimalField(required=False,max_digits=6,decimal_places=2,initial=0.00,label_suffix="",widget= forms.NumberInput(attrs={'class':'form-control'}))
            short_description = forms.CharField(required=False,
                                        label_suffix="",
                                        widget= forms.Textarea(attrs={'class':'form-control','rows':5})
                                        )
            description = forms.CharField(required=False,
                                        label_suffix="",
                                        widget= forms.Textarea(attrs={'class':'form-control'})
                                        )
            state = forms.ChoiceField(required=False,label_suffix="",label='State',choices=STATE_CHOICES, widget=forms.RadioSelect(attrs={'display': 'inline-block'}))
            tags_of_used_technology  = forms.CharField(required=False,label_suffix="",max_length=150,widget= forms.TextInput(attrs={'class':'form-control'}))
            project_url = forms.URLField(required=False,label_suffix="",max_length=100,widget= forms.TextInput(attrs={'class':'form-control'}))
            main_major = forms.CharField(required=False,label_suffix="",max_length=200,widget= forms.TextInput(attrs={'class':'form-control'}))
            progress = forms.ChoiceField(required=False,label_suffix="",label='Progress',choices=[ (x,str(x)+"%") for x in range(1, 100)],widget=forms.Select(attrs={'class':'form-control'}));
            similar_project = forms.CharField(required=False,label_suffix="",max_length=150,widget= forms.TextInput(attrs={'class':'form-control'}))
            release_date = forms.DateField(required=False,label='Released Date',label_suffix="",widget=forms.DateInput(attrs={'class':'datepicker form-control'},format='%m/%d/%Y'))
            class Meta:
                model = Projects
                fields = ['progress','similar_project',
                'name','owner','estimated_time','budget','short_description','description','state',
                'tags_of_used_technology','project_url','main_major','release_date']
            
            #Validation for name Field
            def clean_name(self):
                    cleaned_data = self.cleaned_data
                    if not cleaned_data.get("name"):
                                    raise forms.ValidationError("Project Tiltle is required.")
                    if len(cleaned_data.get("name")) < 15:
                                    raise forms.ValidationError("Project Title should have more then 15 characters and less then 100 characters.")
                    return cleaned_data['name']
            
            #Validation for owner Field
            def clean_owner(self):
                    cleaned_data = self.cleaned_data
                    if not cleaned_data.get("owner"):
                                    raise forms.ValidationError("Project Owner is required.")
                    return cleaned_data['owner']
            #Validation for short_description Field
            def clean_short_description(self):
                    cleaned_data = self.cleaned_data
                    if not cleaned_data.get("short_description"):
                                    raise forms.ValidationError("Short Description is required.")
                    if len(cleaned_data.get("short_description")) < 50:
                                    raise forms.ValidationError("Short Description should have more then 50 characters.")
                    return cleaned_data['short_description']
            #Validation for description Field
            def clean_description(self):
                    cleaned_data = self.cleaned_data
                    if not cleaned_data.get("description"):
                                    raise forms.ValidationError("Description is required.")
                    if len(cleaned_data.get("description")) < 50:
                                    raise forms.ValidationError("Description should have more then 50 characters.")
                    return cleaned_data['description']
            #Validation for similar_project Field
            def clean_similar_project(self):
                    cleaned_data = self.cleaned_data
                    if not cleaned_data.get("similar_project"):
                                    raise forms.ValidationError("similar project is required.")
                    return cleaned_data['similar_project']
            
            def __init__(self, *args, **kwargs):                        
                        super().__init__(*args, **kwargs)
            