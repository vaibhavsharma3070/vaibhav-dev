from django import forms 
from .models import Projects,ProjectFilesAndImages,Responses   #project model
from django.conf import settings
from mainapp.models import CustomUser # All users

class ProjectResponseForm(forms.ModelForm):
            project  =forms.ModelChoiceField(queryset=Projects.objects.all(),label_suffix="",widget= forms.Select(attrs={'class':'form-control'}))
            class Meta:
                model = Responses
                fields = [
                'response','type','project','created_by']

                