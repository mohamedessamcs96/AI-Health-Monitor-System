from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import login ,authenticate,logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
import cv2
import os
import tensorflow
# Create your views here.
from . import used_functions
from .models import DiabetesDiagnose,CancerDiagnose,ReciptImage,User,XrayImage,Complains
from .forms import NewUserForm,DiabetesForm,CancerForm,requreHistory,XRayImageForm

from PIL import Image
from pytesseract import pytesseract
from .forms import ImageForm
import joblib

from django.contrib.auth.decorators import login_required



path_to_tesseract = "AIHealthMonitor/Tesseract-OCR"
diabetes_loaded_model=joblib.load(open('accounts/ML models/PredictDiabetes','rb'))
cancer_loaded_model=joblib.load(open('accounts/ML models/bloodmodel','rb'))
chest_loaded_model=tensorflow.keras.models.load_model('accounts/ML models/best_model.hdf5')

@login_required(login_url='/login/')
def require_history(request):
    form=requreHistory
    return render(request,'requirehistory.html',{'form':form})


@login_required(login_url='/login/')
def others_history(request):
    if request.method=='POST':
        patientid=request.POST.get('ID')
        
        diabetes=(DiabetesDiagnose.objects.filter(patient__identitycard=patientid))
        
    
        cancers=CancerDiagnose.objects.filter(patient__identitycard=patientid)
        prescriptions=ReciptImage.objects.filter(patient__identitycard=patientid)
        chest=XrayImage.objects.filter(patient__identitycard=patientid)
        patient_query=User.objects.filter(identitycard=patientid)
        if(patient_query):
            context={'diabetes':diabetes,'cancers':cancers,'prescriptions':prescriptions,'chests':chest}
            return render(request,'othershistory.html',context)
        else:
            context={'error_message':'No data for that Identitiy Card, Maybe he/she not registered before..'}
            return render(request,'errorMessage.html',context)


    return render(request,'requirehistory.html',context)


@login_required(login_url='/login/')
def get_history(request):

    diabetes=DiabetesDiagnose.objects.filter(patient=request.user)
    cancers=CancerDiagnose.objects.filter(patient=request.user)
    prescriptions=ReciptImage.objects.filter(patient=request.user)
    chest=XrayImage.objects.filter(patient=request.user)
    print("chest")
    print(chest)
    context={'diabetes':diabetes,'cancers':cancers,'prescriptions':prescriptions,'chests':chest}
    return render(request,'history.html',context)


@login_required(login_url='/login/')
def getComplains(request):
    if request.user.is_superuser:
        complains=Complains.objects.all()
        context={'complains':complains}
        return render(request,'getcomplains.html',context)
    else:
        context={'error_message':"Sorry,You're not Authorised to visit this page.."}
        return render(request,'errorMessage.html',context)


@login_required(login_url='/login/')
def user_message(request):
    if request.method=='POST':
        message=request.POST['complains']
        m = Complains(patient=request.user, message=message, phonenumber=(request.user.phonenumber))
        m.save()
        print(message)
        return redirect(homePage)

@login_required(login_url='/login/')
def image_upload_view(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()   
            print("Saved")
            # Get the current instance object to display in the template
            img_obj = form.instance
            print(img_obj)
            print("image instance object "+str(img_obj))

            import os
            from django.conf import settings
            img = Image.open(request.FILES['image'])
            # Providing the tesseract executable
            # location to pytesseract library
            #pytesseract.tesseract_cmd = path_to_tesseract

            # Passing the image object to image_to_string() function
            # This function will extract the text from the image
            text = pytesseract.image_to_string(img)
            print(img_obj)
            print(img_obj.patient)

            # Displaying the extracted text
            print(text[:-1])
            text=text[:-1]
            print("pk")
            print(img_obj.pk)
            from datetime import datetime
            datetime.today().now
            r=ReciptImage.objects.filter(pk=img_obj.pk).update(patient=request.user,description=text)
            
            print("valid")
            return render(request, 'uploadrecipt.html', {'form': form, 'img_obj': img_obj,'description':text})
        return render(request, 'uploadrecipt.html', {'form': form})
        
    else:
        print("get request")
        form = ImageForm()
        return render(request, 'uploadrecipt.html', {'form': form})


################################################
@login_required(login_url='/login/')
def upload_Chest_Photo(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        form = XRayImageForm(request.POST, request.FILES)
        if form.is_valid():
            print("Saved")
            form.save()
            print("Saved")
 
            # Get the current instance object to display in the template
            img_obj = form.instance
            
            import PIL
            import numpy as np
          
            img = request.FILES['image']
            print(img)

            file = request.FILES['image']
            img = Image.open(request.FILES['image'])
            img = np.array(img)
            resized_image = cv2.resize(img, (100,100))
            scaled_image = resized_image.astype("float32")/255.0
            sample_batch = scaled_image.reshape(1, 100, 100, 1) # 1 image, 100, 100 dim , 1 no of chanels
          
            y=chest_loaded_model.predict(sample_batch)
            classification=""
            if(y>0.5):
                classification="Chest cancer"
            else:
                classification="No Chest cancer"

            x=XrayImage.objects.filter(pk=img_obj.pk).update(patient=request.user,classification=classification)

         
            return render(request, 'UploadChestPhoto.html', {'form': form, 'img_obj': img_obj,'classification':y})
        return render(request, 'UploadChestPhoto.html', {'form': form,'classification':y})
        
    else:
        form = XRayImageForm()
        return render(request, 'UploadChestPhoto.html', {'form': form})

########################################################
@login_required(login_url='/login/')
def getDiabetesForm(request):
    form=DiabetesForm()
    context={'form':form}
    return render(request,'checkDiabetes.html',context)



@login_required(login_url='/login/')
def getCancerForm(request):
    form=CancerForm()
    context={'form':form}
    return render(request,'checkCancer.html',context)

@login_required(login_url='/login/')
def bodyCheckup(request):    
    height=request.user.height/100
    weight=request.user.weight
    bmi=weight/(height*height)
    status=""
    if(bmi<18.5):
        status="Under Weight"
    elif(bmi>=18.5 and bmi<24.9):
        status="Over Weight"
    elif(bmi>=25 and bmi<29):
        status="Normal Weight"
    elif(bmi>=30 and bmi<34.9):
        status="Obese"
    elif(bmi<35):
        status="Extremly Obese"
    
    return render(request,'bodyCheckup.html',{'bmi':bmi,'status':status})

@login_required(login_url='/login/')
def waterAvg(request):    
    weightPounds=(request.user.weight)*2.2046226218
    waterInOunces=weightPounds*2/3
    liters=waterInOunces*0.0295735
    
    return render(request,'wateravg.html',{'liters':liters})



@login_required(login_url='/login/')
def checkDiabetes(request):
    form=DiabetesForm() 
    if request.method=='POST':
        patient=request.POST.get('user')
        num_preg=float(request.POST.get('num_preg'))
        glucose_conc=float(request.POST.get('glucose_conc'))
        diastolic_bp=float(request.POST.get('diastolic_bp'))
        thickness=float(request.POST.get('thickness'))
        insulin=float(request.POST.get('insulin'))
        bmi=float(request.POST.get('bmi'))
        diab_pred=float(request.POST.get('diab_pred'))
        age=float(request.POST.get('age'))
        clf=diabetes_loaded_model.predict([[num_preg,glucose_conc,diastolic_bp,thickness,insulin,bmi,diab_pred,age]])
        #clf=clf.map({1:'Has Diabetes',0:'Has No Diabetes'})
        clf=used_functions.diabetes_covert_to_int(clf)
        form=DiabetesForm(request.POST)
        if form.is_valid():
            print("is valid")
            profile=form.save(commit=False)   
            profile.patient=request.user
            profile.save()
            profile.classification=clf
            profile.save()

            objects = DiabetesDiagnose.objects.filter(patient=request.user) 
            context={'results':clf,'form':form,'objects':objects}
            
            print("Objects is:")
            print(objects)
            print("Objects is:")
            return render(request,'result.html',context)
        else:
            print(form.errors.as_data())
            print("is Not valid")
            return redirect('/')

@login_required(login_url='/login/')
def checkCancer(request):
    form=CancerDiagnose() 
    if request.method=='POST':
        patient=request.POST.get('user')
        age=int(request.POST.get('age'))
        bmi=float(request.POST.get('bmi'))
        glucouse=float(request.POST.get('glucouse'))
        insuline=float(request.POST.get('insuline'))
        homa=float(request.POST.get('homa'))
        leptin=float(request.POST.get('leptin'))
        adiponcetin=float(request.POST.get('adiponcetin'))
        mcp=float(request.POST.get('mcp'))
        resistiin=float(request.POST.get('resistiin'))
        print(request.POST)
        clf=cancer_loaded_model.predict([[age,bmi,glucouse,insuline,homa,leptin,adiponcetin,mcp,resistiin]])
        clf=used_functions.covert_to_int(clf)
        print("Clf"+str(clf))
        form=CancerForm(request.POST)
        if form.is_valid():
            print("is valid")
            profile=form.save(commit=False)   
            profile.patient=request.user
            profile.save()
            profile.classification=clf
            profile.save()

            objects = CancerDiagnose.objects.filter(patient=request.user) 
            context={'results':clf,'form':form,'objects':objects}
            
            return render(request,'result.html',context)
        else:
            print(form.errors.as_data())
            print("is Not valid")
            return redirect('/')
    

def homePage(request):
    return render(request,'home.html')

@login_required(login_url='/accounts/login/')
def waitUmblance(request):
    return render(request,'waitambulance.html')

def register_request(request):
    if request.method=="POST":
        form=NewUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            print("register sucessful")
            messages.success(request,"Registration Sucessful")
            return redirect("homepage")
        print("unregister sucessful")
        messages.error(request,"Unsucessful Registration Sucessful invalid operations")
    form=NewUserForm()
    return render(request=request,template_name='register.html',context={'register_form':form})

        
def login_request(request):
    if request.method=="POST":
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                print("logged")
                messages.info(request,f"You are logged is as {username}.")
                return redirect("homepage")
            else:
                print("invalid username and password")
                messages.error(request,"invalid username and password")
        else:
                print("not valid form")
                messages.error(request,"not valid form")
    
    form=AuthenticationForm()
    return render(request=request,template_name='login.html',context={'login_form':form})

def logout_request(request):
    logout(request)
    messages.info(request,"You have sucessfully loggedout")
    return redirect("login")






