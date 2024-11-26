## Analyse Statistique des Données d'Assurance

Ce projet a pour objectif d'analyser les données d'assurance à travers des statistiques descriptives et des tests d'ANOVA afin d'évaluer les impacts des facteurs tels que la région et le type d'assurance sur le chiffre d'affaires (C.A.).

---

## Prérequis

Avant d'exécuter ce projet, assurez-vous d'avoir les logiciels et packages suivants installés :

- **R** (Version >= 4.0)
- Les bibliothèques R nécessaires :
  - `stats`
  - `readxl`

Pour installer les bibliothèques manquantes, exécutez :

```R
install.packages("readxl")
```

---

## Données

Les données utilisées sont contenues dans un fichier Excel nommé `TP2.xlsx`. Ce fichier doit contenir les colonnes suivantes :
- **Région** : Catégories géographiques des données.
- **Type d'assurance** : Types d'assurance analysés.
- **C.A. (en milliers)** : Chiffre d'affaires en milliers d'unités monétaires.

---

## Instructions

### 1. Importation des données

Le fichier `TP2.xlsx` est importé en utilisant la bibliothèque `readxl`. Assurez-vous que le fichier est dans le répertoire de travail courant ou fournissez son chemin absolu.

```R
data = read_excel("TP2.xlsx")
```

### 2. Statistiques descriptives

Résumé des données avec la fonction `summary()` pour avoir une vue globale des distributions des variables.

```R
summary(data)
```

### 3. Visualisation

Création de boîtes à moustaches pour comparer le chiffre d'affaires en fonction de la région et du type d'assurance.

```R
boxplot(data$`C.A. (en milliers)` ~ data$Région * data$`Type d'assurance`, main="Boîte à Moustache du C.A. par type d'assurance et région")
```

### 4. Analyse ANOVA

#### ANOVA avec interaction

Un modèle d'ANOVA à deux facteurs avec interaction est ajusté pour évaluer l'effet combiné des facteurs.

```R
modele <- aov(data$`C.A. (en milliers)` ~ data$Région * data$`Type d'assurance`, data=data)
summary(modele)
```

#### ANOVA sans interaction

Une analyse sans interaction est également réalisée pour examiner les effets individuels des facteurs.

```R
anov <- aov(data$`C.A. (en milliers)` ~ data$Région + data$`Type d'assurance`, data=data)
summary(anov)
```


## Résultats

- **ANOVA avec interaction** :
  - La probabilité critique associée à l'effet d'interaction est supérieure à 0.05, ce qui indique que l'interaction entre les deux facteurs n'est pas significative.

- **ANOVA sans interaction** :
  - Les facteurs **Région** et **Type d'assurance** pris individuellement ne montrent pas d'effet significatif sur le chiffre d'affaires.


## Utilisation

1. Clonez ce dépôt.
2. Placez le fichier `TP2.xlsx` dans le répertoire.
3. Exécutez le script R fourni pour analyser les données.


## Auteur

Réalisé par **MBASSI ATANGANA**, étudiant en Master 1 Data Sciences à l'Université de Yaoundé 1.
