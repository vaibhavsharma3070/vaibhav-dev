from django import forms 
from .models import Projects,ProjectFilesAndImages   #project model
from django.conf import settings
from mainapp.models import CustomUser # All users

class ProjectFilesAndImagesForm(forms.ModelForm):
            project  =forms.ModelChoiceField(queryset=Projects.objects.all(),label_suffix="",widget= forms.Select(attrs={'class':'form-control'}))
            class Meta:
                model = ProjectFilesAndImages
                fields = [
                'id','file','type','subtype','project']
                