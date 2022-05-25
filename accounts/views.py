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
from .models import DiabetesDiagnose,CancerDiagnose,ReciptImage,User,XrayImage
from .forms import NewUserForm,DiabetesForm,CancerForm,requreHistory,XRayImageForm

from PIL import Image
from pytesseract import pytesseract
from .forms import ImageForm
import joblib

#diabetes_loaded_model=joblib.load(open(r"C:\Users\THE LAPTOP SHOP\Desktop\HealthMonitor\AIHealthMonitor\accounts\ML models\PredictDiabetes", 'rb'))
#cancer_loaded_model=joblib.load(open(r"C:\Users\THE LAPTOP SHOP\Desktop\HealthMonitor\AIHealthMonitor\accounts\ML models\bloodmodel", 'rb'))
diabetes_loaded_model=joblib.load(open('accounts/ML models/PredictDiabetes','rb'))
cancer_loaded_model=joblib.load(open('accounts/ML models/bloodmodel','rb'))
chest_loaded_model=tensorflow.keras.models.load_model('accounts/ML models/best_model.hdf5')
def require_history(request):
    form=requreHistory
    return render(request,'requirehistory.html',{'form':form})



def others_history(request):
    if request.method=='POST':
        patientid=request.POST.get('ID')
        print(request.user.identitycard)
        print(patientid)
        patient_query=User.objects.filter(identitycard=patientid)
        patientusername=((patient_query.values('username'))[0]['username'])
        diabetes=(DiabetesDiagnose.objects.filter(patient__identitycard=patientid))
        print(diabetes)
        
        #12312312312313
        print(type(patientusername))
        print(type(request.user))
        #print(type(((diabetes.values('classification'))[0]['classification'])))
        cancers=CancerDiagnose.objects.filter(patient__identitycard=patientid)
        print(cancers)
        #print(type(((diabetes.values('classification'))[0]['classification'])))
        prescriptions=ReciptImage.objects.filter(patient=request.user)
        #print(type(((diabetes.values('classification'))[0]['classification'])))
        print(prescriptions)
        context={'diabetes':diabetes,'cancers':cancers,'prescriptions':prescriptions}
        return render(request,'othershistory.html',context)
    return render(request,'requirehistory.html',context)

def get_history(request):
    #prescriptions=ReciptImage.objects.filter(patient=request.user)
    #print(prescriptions.values)
    diabetes=DiabetesDiagnose.objects.filter(patient=request.user)
    cancers=CancerDiagnose.objects.filter(patient=request.user)
    prescriptions=ReciptImage.objects.filter(patient=request.user)
    #print(type(((diabetes.values('classification'))[0]['classification'])))
    print(prescriptions)
    context={'diabetes':diabetes,'cancers':cancers,'prescriptions':prescriptions}
    return render(request,'history.html',context)



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
            #uploadedImage = request.FILES
            print("image instance object "+str(img_obj))
            #print("request filses "+str(request.FILES['upload']))
            # Defining paths to tesseract.exe
            # and the image we would be using
            path_to_tesseract = r"C:\Users\THE LAPTOP SHOP\Desktop\HealthMonitor\AIHealthMonitor\Tesseract-OCR"
            #image_path = r"Python-language.png"
            #image_path=uploadedImage
            # Opening the image & storing it in an image object
            #loadedimg = ReciptImage.objects.filter(title=img_obj)
            #loadedimg = ReciptImage.objects.filter(patient=request.user,title=img_obj)
            #print("loaded image"+str(loadedimg))
            
            #image_data = open("C:/Users/THE LAPTOP SHOP/Desktop/HealthMonitor/AIHealthMonitor"+img_obj.image.url, "rb").read()
            #print(image_data)
            #print(loadedimg.values_list('image', flat=True)[0])
            #print(ReciptImage.objects.values('image'))
            #loaded_image=(ReciptImage.objects.filter(title=img_obj).values('image'))[0]['image']
            #print(loaded_image)
            #print(ReciptImage.objects.filter(title=img_obj).path)
            #data= open(os.path.join(settings.MEDIA_ROOT, str(img_obj.image.url)),'rb').read()
            img = Image.open(r"C:/Users/THE LAPTOP SHOP/Desktop/HealthMonitor/AIHealthMonitor"+img_obj.image.url)

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
            #r = ReciptImage(patient=request.user,description=text,pk=img_obj.pk,created=datetime.today().now().year)
            #r.save()
            
            print("valid")
            return render(request, 'uploadrecipt.html', {'form': form, 'img_obj': img_obj,'description':text})
        return render(request, 'uploadrecipt.html', {'form': form})
        
    else:
        print("get request")
        form = ImageForm()
        return render(request, 'uploadrecipt.html', {'form': form})


################################################

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
            img = Image.open(r"C:/Users/THE LAPTOP SHOP/Desktop/HealthMonitor/AIHealthMonitor"+img_obj.image.url)
            print("img")
            print(img)
            loaded_image=(XrayImage.objects.filter(title=img_obj).values('image'))[0]['image']
            #print(loaded_image)
            #img='AIHealthMonitor/'+loaded_image
            import PIL
            import numpy as np
            print("imgg")
            print(img)
          
            print(np.array(img))
            from keras.preprocessing import image
            import tensorflow as tf
            img = request.FILES['image']
            print(img)
            #img = image.load_img(myfile, target_size=(100, 100))
            #img= tf.image.resize(myfile,(100,100))
            #img= tf.keras.layers.Resizing(img,100,100)
            #image = cv2.imread(request.FILES['image'])
            file = request.FILES['image']
            img = Image.open(request.FILES['image'])
            img = np.array(img)
            resized_image = cv2.resize(img, (100,100))
            scaled_image = resized_image.astype("float32")/255.0
            sample_batch = scaled_image.reshape(1, 100, 100, 1) # 1 image, 100, 100 dim , 1 no of chanels
            #npimg = np.fromfile(file, np.uint8)
            #file = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
            #resized = cv2.resize(file, (100,100))
            #img = image.img_to_array(img)
            #img = np.expand_dims(img, axis=0)
            #img = img/255
            #img=img.reshape(1, 100, 100, 1)
            y=chest_loaded_model.predict(sample_batch)
            #gray_image = cv2.imread(img, 0)

            """
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            resized_image = cv2.resize(gray_image, (100,100), PIL.Image.ANTIALIAS)
            scaled_image = resized_image.astype("float32")/255.0
            sample_batch = scaled_image.reshape(1, 100, 100, 1) # 1 image, 100, 100 dim , 1 no of chanels
            
            print("Classification :")
            y=chest_loaded_model.predict(sample_batch)
            """
            #y=0
            print(y)
            return render(request, 'UploadChestPhoto.html', {'form': form, 'img_obj': img_obj,'classification':y})
        return render(request, 'UploadChestPhoto.html', {'form': form,'classification':y})
        
    else:
        form = XRayImageForm()
        return render(request, 'UploadChestPhoto.html', {'form': form})

########################################################

def getDiabetesForm(request):
    form=DiabetesForm()
    context={'form':form}
    return render(request,'checkDiabetes.html',context)

def getCancerForm(request):
    form=CancerForm()
    context={'form':form}
    return render(request,'checkCancer.html',context)

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






