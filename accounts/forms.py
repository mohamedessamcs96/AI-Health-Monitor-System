from cProfile import label
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm 

#from django.contrib.auth.models import User

from .models import *

#Create the form 

class NewUserForm(UserCreationForm):
    error_css_class='error-field'
    required_css_class='required-field'
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"col-md-6","style":'max-width: 20em',"id":"","placeholder":"username"}))
    email=forms.EmailField(widget=forms.TextInput(attrs={"class":"col-md-6","style":"max-width: 20em","id":"","placeholder":"email"}))
    phonenumber=forms.CharField(widget=forms.TextInput(attrs={"class":"col-md-6","style":"max-width: 20em","id":"","placeholder":"phonenumber"}))
    birthdate=forms.IntegerField(widget=forms.TextInput(attrs={"class":"col-md-6","style":"max-width: 20em","id":"","placeholder":"birthdate"}))
    identitycard=forms.CharField(widget=forms.TextInput(attrs={"class":"col-md-6","style":"max-width: 20em","id":"","placeholder":"identitycard"}))
    height=forms.IntegerField(widget=forms.TextInput(attrs={"class":"col-md-6","style":"max-width: 20em","id":"","placeholder":"height"}))
    weight=forms.IntegerField(widget=forms.TextInput(attrs={"class":"col-md-6","style":"max-width: 20em","id":"","placeholder":"weight"}))
    password1: forms.Field
    password2: forms.Field
    class Meta:
        model=User
        fields=('username','email','phonenumber','birthdate','gender','identitycard','bloodtype','height','weight','password1','password2')




class DiabetesForm(forms.ModelForm):
    error_css_class='error-field'
    required_css_class='required-field'
    num_preg=forms.IntegerField(widget=forms.TextInput(attrs={"class":"col-md-6","style":'max-width: 20em',"id":"","placeholder":"num_preg if woman"}))
    glucose_conc=forms.IntegerField(widget=forms.TextInput(attrs={"class":"col-md-6","style":"max-width: 20em","id":"","placeholder":"glucose_conc"}))
    diastolic_bp=forms.IntegerField(widget=forms.TextInput(attrs={"class":"col-md-6","style":"max-width: 20em","id":"","placeholder":"diastolic_bp"}))
    thickness=forms.IntegerField(widget=forms.TextInput(attrs={"class":"col-md-6","style":"max-width: 20em","id":"","placeholder":"thickness"}))
    insulin=forms.IntegerField(widget=forms.TextInput(attrs={"class":"col-md-6","style":"max-width: 20em","id":"","placeholder":"insulin"}))
    bmi=forms.IntegerField(widget=forms.TextInput(attrs={"class":"col-md-6","style":"max-width: 20em","id":"","placeholder":"bmi"}))
    diab_pred=forms.IntegerField(widget=forms.TextInput(attrs={"class":"col-md-6","style":"max-width: 20em","id":"","placeholder":"diab_pred"}))
    age=forms.IntegerField(widget=forms.TextInput(attrs={"class":"col-md-6","style":"max-width: 20em","id":"","placeholder":"age"}))

    class Meta:
        model=DiabetesDiagnose
        fields=('num_preg','glucose_conc','diastolic_bp','thickness','insulin','bmi','diab_pred','age')
       

class CancerForm(forms.ModelForm):
    error_css_class='error-field'
    required_css_class='required-field'
    age=forms.IntegerField(widget=forms.TextInput(attrs={"class":"col-md-6","style":'max-width: 20em',"id":"","placeholder":"age"}))
    bmi=forms.IntegerField(widget=forms.TextInput(attrs={"class":"col-md-6","style":"max-width: 20em","id":"","placeholder":"bmi"}))
    glucouse=forms.IntegerField(widget=forms.TextInput(attrs={"class":"col-md-6","style":"max-width: 20em","id":"","placeholder":"glucouse"}))
    insuline=forms.IntegerField(widget=forms.TextInput(attrs={"class":"col-md-6","style":"max-width: 20em","id":"","placeholder":"insuline"}))
    homa=forms.IntegerField(widget=forms.TextInput(attrs={"class":"col-md-6","style":"max-width: 20em","id":"","placeholder":"homa"}))
    leptin=forms.IntegerField(widget=forms.TextInput(attrs={"class":"col-md-6","style":"max-width: 20em","id":"","placeholder":"leptin"}))
    adiponcetin=forms.IntegerField(widget=forms.TextInput(attrs={"class":"col-md-6","style":"max-width: 20em","id":"","placeholder":"adiponcetin"}))
    resistiin=forms.IntegerField(widget=forms.TextInput(attrs={"class":"col-md-6","style":"max-width: 20em","id":"","placeholder":"resistiin"}))
    mcp=forms.IntegerField(widget=forms.TextInput(attrs={"class":"col-md-6","style":"max-width: 20em","id":"","placeholder":"mcp"}))
    class Meta:
        model=CancerDiagnose
        fields=('age','bmi','glucouse','insuline','homa','leptin','adiponcetin','resistiin','mcp')


from .models import ReciptImage


class ImageForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = ReciptImage
        fields = ('title', 'image')

class XRayImageForm(forms.ModelForm):
    """Form for the image model"""

    
    class Meta:
            model = XrayImage
            fields = ('title', 'image')




class requreHistory(forms.Form):
    ID=forms.CharField(max_length=15)