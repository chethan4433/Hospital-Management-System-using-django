from django.urls import path
from . import views

urlpatterns =[

    # AUTHENTICATION
    path('', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('profile/', views.profile, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('update_password/', views.update_password, name='update_password'),
    path('signout/', views.signout, name='signout'),


    # CRUD
    path('home/', views.home, name='home'),
    path('patient_list/', views.patient_list, name='patient_list'),
    path('update_patient/<int:pk>', views.update_patient, name='update_patient'),
    path('delete_patient/<int:pk>', views.delete_patient, name='delete_patient'),
]