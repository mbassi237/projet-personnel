from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import PatientSerializer, FrottisSerializer
from rest_framework.decorators import api_view
from .models import Patient, Frottis, Rapport
import tensorflow as tf
import os 
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from rest_framework import status 
from tensorflow.keras.preprocessing import image
import numpy as np
from tensorflow.keras.models import load_model
from django.core.files.storage import default_storage
from django.http import FileResponse
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.contrib import messages
import os
import json
from django.http import HttpResponse
# Create your views here.

# Enregistrer patient
@api_view(['GET', 'POST'])
def EnregistrerPatient(request):
    patient_list = Patient.objects.all()
    if request.method == 'POST':
        data = Patient(
            nom=request.POST['nom'],
            sexe=request.POST['sexe'],
            age=request.POST['age'],
            email=request.POST['email']
        )
        data.save()
        identifiant = data.id
        data.code_patient = "P" + str(identifiant).zfill(24) # Generer automatiquement code_patient
        data.save()
        #response = HttpResponse(json.dumps({'reponse': 'patient bien enregistree'}), content_type='application/json')
    return render(request, 'doameki/patientformulaire.html', {'patient_list': patient_list})



def DeletePatient(request, pk):
    patient_delete = get_object_or_404(Patient, id=pk)
    if request.method == 'POST':
        patient_delete.delete()
        return redirect('patient-create')
    context = {'bulletin_delete' : patient_delete}
    return render(request, 'doameki/patientformulaire.html')


# fonction pour la detection du plasmodium avec le model CNN
classnames = ['Parasitized', 'Uninfected']
def detection_malaria(image_path, model_path):
    # Chargeons le modele sauvegarde
    model = load_model(model_path)
    # Charger et pretraitons l'image
    img = image.load_img(image_path, target_size=(32, 32))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0 # normaliser l'image
    
    # Predire la classe
    prediction = model.predict(img_array).flatten() # transformation en tableau 1D
    
    # Creation d'un dictionnaire pour les resultats
    results = {
        classnames[i]: round(float(prediction[i]), ndigits=1)
        for i in range(len(classnames))
    }
    
    # Tri par probabilites decroissantes
    resultats_tries = sorted(results.items(), key=lambda x: x[1], reverse=True)
    return resultats_tries


# Analyser une image de frottis sanguin d'un patient
@api_view(['GET', 'POST'])
def AnalyseFrottis(request):
    patients = Patient.objects.all()  # Récupération des patients pour affichage dans le formulaire
    if request.method == 'POST':
        patient_id = request.POST.get('id_patient')  # Récupération de l'ID du patient depuis le formulaire
        patient = get_object_or_404(Patient, id=patient_id)  # Vérification de l'existence du patient

        serializer = FrottisSerializer(data=request.data)
        if serializer.is_valid():
            frottis_instance = serializer.save(id_patient=patient)  # Enregistrement du frottis

            # Lancement de l'analyse avec le modèle CNN
            image_path = frottis_instance.image.path
            model_path = 'C:/Users/pc/Malaria_Detection/models3/shape_classifier.h5'
            resultat_analyse = detection_malaria(image_path, model_path)

            # Mise à jour du frottis avec le statut obtenu
            frottis_instance.status = resultat_analyse
            frottis_instance.save()

            return render(request, 'doameki/rapport.html', {
                'resultats': resultat_analyse,
                'patients': patients
            })
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return render(request, 'doameki/rapport.html', {'patients': patients})




@api_view(['POST'])
def GenererRapport(request):
    patient_id = request.data.get('id_patient')  # Récupération de l'ID du patient
    patient = get_object_or_404(Patient, id=patient_id)  # Vérification du patient

    # Vérification du frottis le plus récent du patient
    frottis = Frottis.objects.filter(id_patient=patient).order_by('-id').first()
    if not frottis:
        return Response({"error": "Aucun frottis trouvé pour ce patient"}, status=status.HTTP_404_NOT_FOUND)

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    # En-tête du rapport
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 770, "Rapport d'analyse Frottis")
    p.line(100, 760, 500, 760)  # Ligne de séparation

    # Informations du patient
    p.setFont("Helvetica", 12)
    p.drawString(100, 730, f"Nom: {patient.nom}")
    p.drawString(100, 710, f"Identifiant: {patient.code_patient}")
    p.drawString(100, 690, f"Sexe: {patient.sexe}")
    p.drawString(100, 670, f"Âge: {patient.age} ans")
    
    # Résultat de l'analyse
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, 640, "🔍 Résultats de l'analyse :")
    p.setFont("Helvetica", 12)
    p.drawString(100, 620, f"Statut du frottis : {frottis.status}")

    # Finalisation du PDF
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"rapport_{patient.nom}.pdf")




def interface_analyse(request):
    return render(request, 'doameki/master.html')
