from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',views.homePage,name='homepage'),
    path('uploadchestphoto/',views.upload_Chest_Photo,name='uploadchestphoto'),
    path('gethistory/',views.get_history,name='gethistory'),
    path('getcomplains/',views.getComplains,name='getcomplains'),
    path('wateravg/',views.waterAvg ,name='wateravg'),
    path('message/',views.user_message ,name='message'),
    path('waitumblance/',views.waitUmblance ,name='waitumblance'),
    path('checkdiabetes/',views.checkDiabetes,name='checkdiabetes'),
    path('othershistory/',views.others_history,name='othershistory'),
    path('requirehistory/',views.require_history,name='requirehistory'),
    path('bodycheckup/',views.bodyCheckup,name='bodycheckup'),
    path('uploadrecipt/',views.image_upload_view,name='uploadrecipt'),
    #path('getrecipt/',views.getRecipt,name='getrecipt'),
    path('getdiabetesform/',views.getDiabetesForm,name='getdiabetesform'),
    path('checkcancer/',views.checkCancer,name='checkcancer'),
    path('getcancerform/',views.getCancerForm,name='getcancerform'),
    path('register/',views.register_request ,name="register"),
    path('login/',views.login_request ,name="login"),
    path('logout/',views.logout_request ,name="logout")
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)