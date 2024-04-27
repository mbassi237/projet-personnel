library(stats)
library(readxl)

## Importer les donnees
data = read_excel("TP2.xlsx")

## Statistique descriptive des donnees
summary(data)

## Boites a moustaches des valeurs par combinaison de facteurs
boxplot(data$`C.A. (en milliers)` ~ data$Région * data$`Type d'assurance`,main="Boite a Moustache du C.A de chaque type d'assurance dans leur region")

# ANOVA a deux facteurs
modele <- aov(data$`C.A. (en milliers)` ~ data$Région*data$`Type d'assurance`, data=data)
summary(modele) ## La probabilite critique(0.658) associe a l'effet d'interaction est superieur
                ## au seuil (0.05) donc l'hypothese H0 est acceptee on conclut a la non-significativite
                ##de l'interaction.

## ANOVA sans interaction
anov = aov(data$`C.A. (en milliers)` ~ data$Région+data$`Type d'assurance`, data=data)
summary(anov) ##les deux facteurs region et type d'assurance ne sont pas toujours significatifs(0.182 et 0.256 > 0.05)
              ##donc y'a pas d'effet de la region et d'effet du type d'assurance sur le C.A d'une assurance
