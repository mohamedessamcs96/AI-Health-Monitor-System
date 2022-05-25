from django.db import models

from django.contrib.auth.models import User,AbstractUser

# Create your models here.



   
    

class User(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    BLOOD_CHOICES = (
        ('A', 'A'),
        ('A+', 'A+'),
        ('B+', 'B+'),
        ('B', 'B'),
        ('O', 'O'),
        ('O+', 'O+'),
        ('AB', 'AB'),
        ('AB+', 'AB+'),
    )
    email=models.EmailField(max_length=50,unique=True)
    USERNAME_FILED='email'
    fields_required=['email']
    phonenumber=models.CharField(max_length=15, default='+20')
    birthdate=models.IntegerField(default=1996)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='Male')
    identitycard=models.CharField(max_length=20,primary_key=True)
    bloodtype=models.CharField(max_length=3, choices=BLOOD_CHOICES, default='A')
    height=models.IntegerField(default=160)
    weight=models.IntegerField(default=70)
    

class DiabetesDiagnose(models.Model):
    patient=models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    num_preg=models.IntegerField()
    glucose_conc=models.IntegerField()
    diastolic_bp=models.IntegerField()
    thickness=models.IntegerField()
    insulin=models.IntegerField()
    bmi=models.IntegerField()
    diab_pred=models.IntegerField()
    age=models.IntegerField()
    created=models.DateTimeField(auto_now_add=True)
    classification=models.CharField(max_length=15,null=False)
    def __str__(self):
        return self.patient.username +'  has Diabetes is? '+self.classification

class CancerDiagnose(models.Model):
    patient=models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    age=models.IntegerField()
    bmi=models.FloatField()
    glucouse=models.FloatField()
    insuline=models.FloatField()
    homa=models.FloatField()
    leptin=models.FloatField()
    adiponcetin=models.FloatField()
    resistiin=models.FloatField()
    mcp=models.FloatField()
    created=models.DateTimeField(auto_now_add=True)
    classification=models.CharField(max_length=15,null=False)
    def __str__(self):
        return self.patient.username +'  has Cancer is? '+self.classification

    


class ReciptImage(models.Model):
    patient=models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')
    created=models.DateTimeField(auto_now_add=True)
    description=models.CharField(max_length=200)


    def __str__(self):
        return self.title


class XrayImage(models.Model):
    patient=models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')
    created=models.DateTimeField(auto_now_add=True)
    classification=models.CharField(max_length=10)


    def __str__(self):
        return self.title

#Foo.objects.filter(gender = 'M').update(gender = 'H')