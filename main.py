import streamlit as st
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


### CREATION DE L'INTERFACE GRAPHIQUE
st.set_page_config(
    page_title="Doabra",
    page_icon='Doabra/Doabra.png'
)
with st.container():
    st.write("Developpe par: MBASSI ATANGANA")
st.image('Doabra/Doabra.png', width=200)
st.write('''
# Bienvenue sur votre Application de prediction de l'etat de sante d'un individu
Entrez vos parametres physiologiques:
''')

temperature = st.number_input("Entrez votre température (°C) :", min_value=35.0, max_value=42.0, step=0.1)
pouls = st.number_input("Entrez votre fréquence cardiaque (bpm) :", min_value=40, max_value=150, step=1)
oxygene = st.number_input("Entrez votre taux d'oxygène (%) :", min_value=90, max_value=100, step=1)
glycemie = st.number_input("Entrez votre glycémie (mg/dL) :", min_value=70, max_value=300, step=1)
tension = st.number_input("Entrez votre tension artérielle (mmHg) :", min_value=80, max_value=150, step=1)

### MODELE DE PREDICTION
data = pd.read_csv("maladie_observations.csv")

#nombre de valeurs manquantes par variables
data.isna().sum()

liste = ['temperature', 'pouls', 'oxygene']
for i in liste:
    data[i] = data[i].fillna(data[i].mean())

#remplacement des valeurs aberantes par la moyenne
data['oxygene'] = data['oxygene'].where(~data['oxygene'].between(300 , 600) , data.mean())
data['temperature'] = data['temperature'].where(~data['temperature'].between(250 , 530) , data.mean())
data['pouls'] = data['pouls'].where(~data['pouls'].between(280 , 600) , data.mean())

#supprimer les valeurs trop grande et infinies
new = data[np.isfinite(data).all(1)]

#creature des features et du label
X = new.drop('label', axis=1)
Y = new['label']

#separation des donnees pour les tests et l'entrainement
X_train , X_test , Y_train , Y_test = train_test_split(X,Y , test_size=0.2 , random_state=0)
print(X_test.shape)
print(X_train.shape)

#creation du modele
modele = LogisticRegression(penalty=None)
modele.fit(X_train , Y_train)

#Tester le modele
#predictions = modele.predict(df)
#print(predictions)
#print(Y_test)
if st.button("Prédire"):
    # Préparer les données d'entrée
    input_data = np.array([[float(temperature), float(pouls), float(pouls), float(glycemie), int(tension)]])
    predictions = modele.predict(input_data)
    # Afficher les résultats
    if predictions[0] == 0:
        st.write("Vous êtes en état de santé normal.")
    else:
        st.write("Vous êtes probablement malade. Consultez un médecin dès que possible pour plus de précisions")


