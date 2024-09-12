from django.urls import path
from . import  views

urlpatterns=[
     path('', views.main, name="main"),
     path('home/', views.homepage, name="homepage"),
     path('activity/', views.recent_activity, name="activity"),
     path('add/upload-img/', views.uploadimg, name="uploadimg"),
     path('successpage/', views.successpage, name="successpage"),
     path('feature/', views.feature, name="feature"),
     path('about/', views.about, name="about"),
     path('edit/<str:imgpath>/', views.editlist, name='edit'),
     path('edit/editimage/flipimage/<str:imgname>/', views.flipimage, name='flip'),
     path('edit/editimage/mirrorimage/<str:imgname>/', views.mirrorimage, name='mirrorimage'),
     path('edit/editimage/rotate/<str:imgname>/', views.rotate, name='rotate'),
     path('edit/editimage/grayscale/<str:imgname>/', views.grayscale, name='grayscale'),
     path('edit/editimage/contrast/<str:imgname>/', views.adjust_contrast, name='contrast'),
     path('edit/editimage/brightness/<str:imgname>/', views.brightness, name='brightness'),
     path('edit/editimage/blur/<str:imgname>/', views.blur, name='blur'),
     path('edit/editimage/saturation/<str:imgname>/', views.saturation, name='saturation'),
     path('edit/editimage/invert/<str:imgname>/', views.invert, name='invert'),
     path('edit/editimage/sharpness/<str:imgname>/', views.sharpness, name='sharpness'),
     path('<str:imgname>/', views.imageView, name="imageView"),


]