from django import forms
from django.contrib.auth.models import User
from django.views.generic import CreateView
from .models import ques

class quesCreateView(forms.ModelForm):
	class Meta:
	    model  = ques
	    fields = ['question']