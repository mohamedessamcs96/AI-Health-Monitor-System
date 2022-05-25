from cProfile import label
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm 

#from django.contrib.auth.models import User

from .models import *

#Create the form 

class NewUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=('username','email','phonenumber','birthdate','gender','identitycard','bloodtype','height','weight')




class DiabetesForm(forms.ModelForm):
    class Meta:
        model=DiabetesDiagnose
        fields=('num_preg','glucose_conc','diastolic_bp','thickness','insulin','bmi','diab_pred','age')
        widgets = {
            'num_preg': forms.TextInput(attrs={'class':'col-xs-2','size': '2'}),
            #'glucose_conc': forms.TextInput(attrs={'class':'col-xs-2'}),
            'diastolic_bp': forms.TextInput(attrs={'class':'col-xs-2'}),
            #'thickness': forms.TextInput(attrs={'class':'col-xs-2'}),
            'insulin': forms.TextInput(attrs={'class':'col-xs-2'}),
            #'bmi': forms.TextInput(attrs={'class':'col-xs-2'}),
            'diab_pred': forms.TextInput(attrs={'class':'col-xs-2'}),
            #'age': forms.TextInput(attrs={'class':'col-xs-2'}),
        }  
       
        """
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['num_preg'].widget.attrs.update(label='num_preg')
            self.fields['num_preg'].widget.attrs.update(size='2')
            
            #fields.widget.attrs.update({'num_preg' : 'num_preg','glucose_conc':'glucose_conc','diastolic_bp':'diastolic_bp','thickness':'thickness','insulin':'insulin','bmi':'bmi','diab_pred':'diab_pred','age':'age'})
        """

class CancerForm(forms.ModelForm):
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

"""  
    def save(self):
        photo = super(XrayImage,self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')
        from PIL import Image
        import cv2

        image = Image.open(photo.file)
        gray_image = cv2.imread(image, 0)
        resized_image = cv2.resize(gray_image, (100,100))
        scaled_image = resized_image.astype("float32")/255.0
        sample_batch = scaled_image.reshape(1, 100, 100, 1) # 1 image, 100, 100 dim , 1 no of chanels
        sample_batch.save(photo.file.path)

        return photo
"""



class requreHistory(forms.Form):
    ID=forms.CharField(max_length=15)