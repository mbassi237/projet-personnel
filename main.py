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
Bienvenue sur votre Application de prediction de l'etat de sante d'un individu
''')

st.sidebar.header("Entrez vos parametres physiologiques:")

def user_input():
    temperature = st.sidebar.slider('Temperature corporelle', 15.30 , 50.65, 36.00)
    pouls = st.sidebar.slider('rythme cardiaque', 60.00, 200.00, 180.00)
    oxygene = st.sidebar.slider('Taux oxygene dans le sang', 40.25, 250.00, 95.00)
    glycemie = st.sidebar.slider('Taux de glycemie', 10.00, 200.00, 110.00)
    tension = st.sidebar.slider('Tension arterielle', 50, 200, 84)
    data = {
        'temperature': temperature,
        'pouls': pouls,
        'oxygene': oxygene,
        'glycemie': glycemie,
        'tension': tension
    }
    parametres = pd.DataFrame(data, index=[0])
    return parametres



df = user_input()
st.subheader("Trouver l'etat de sante de cet l'individu:")
st.write(df)

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
predictions = modele.predict(df)
#print(predictions)
#print(Y_test)

st.subheader("votre etat de sante :")
if predictions == 1:
    st.write("Vous etes malade")
    st.write("Nous vous recommandons de vous rendre au plutôt dans une structure sanitaire et effectuer des examens pour en savoir plus.")
else:
    st.write("Vous etes en etat de sante normal.")
    st.write("Veuillez quand même boire beaucoup d'eau, manger sain et faire de l'exercice physique régulier")
