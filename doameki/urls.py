from django.urls import path
from . import views
from .views import EnregistrerPatient, AnalyseFrottis, GenererRapport, interface_analyse, DeletePatient

urlpatterns = [
    path('patients/', EnregistrerPatient, name='patient-create'),
    path('analysefrottis/', AnalyseFrottis, name='analyse-frottis'),
    path('rapportpdf/', GenererRapport, name='generer-rapport'),
    path('master/', views.interface_analyse, name='home'),
    path('deletepatients/<int:pk>/', views.DeletePatient,name='delete-patient' ),
    
]
