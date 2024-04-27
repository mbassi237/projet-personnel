## Importation des librairies
library(car)
library(dplyr)
library(lmtest)

## importation des donnees
data(mtcars)

##type des variables du jeu de donnees
typeof(mtcars$mpg)
typeof(mtcars$cyl)
typeof(mtcars$disp)
typeof(mtcars$hp)
typeof(mtcars$drat)
typeof(mtcars$wt)
typeof(mtcars$qsec)
typeof(mtcars$vs)

## 1.	Etudions les corrélations linéaires entre les variables explicatives deux à deux
newdata <- cbind(mtcars$mpg, mtcars$cyl, mtcars$disp, mtcars$hp, mtcars$drat, mtcars$wt, mtcars$qsec, mtcars$vs, mtcars$am, mtcars$gear, mtcars$carb)
newdata
pairs(newdata)
## correlation
cor(mtcars[,c("cyl","disp","hp","drat","wt","qsec","vs" , "am" , "gear" , "carb" , "mpg")], use="complete.obs")

##Ajustement du modele
modele = lm(mtcars$mpg ~ mtcars$hp+mtcars$drat+mtcars$vs+mtcars$am)
summary(modele)

## Evaluons la multi-collinearite par les VIFs
vif(modele)

## Evaluer les hypothèses de normalité et d’homoscédasticité des résidus du modèle complet

#Obtenir les residus de notre modele
modele$residuals

# Testons la normalite des residus , sur le graphique nous comparons la distribution des points a la ligne droite
qqnorm(modele$residuals) ##La normalite est plausible
#Test de shapiro-wilk, nous avons une normalite non rejetee par le modele
shapiro.test(modele$residuals)

# Tester l'homoscedasticite
# graphique des residus vs valeurs predites ,homogenite de la dispersion des points
plot(modele$fitted.values, modele$residuals , title("graphique des residus vs valeurs predites"), xlab = "valeurs predites", ylab = "residus")

# Test de white/ Test de Breusch-Pagan 
bptest(modele) #l'homoscedasite est non rejetee , la variance des residus est constante pour toutes les valeurs des variables explicatives
