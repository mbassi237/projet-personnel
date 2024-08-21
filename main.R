#  Étude de la Violence Domestique en fonction des Régions

## Importation du jeu de donnees
dhs_ipv <- read.csv("dhs_ipv.csv")

str(dhs_ipv)

## Verification des valeurs manquantes
sum(is.na(dhs_ipv))
sum(is.na(dhs_ipv$beat_burnfood))
sum(is.na(dhs_ipv$beat_goesout))
sum(is.na(dhs_ipv$sec_school))
sum(is.na(dhs_ipv$no_media))
sum(is.na(dhs_ipv$country))
sum(is.na(dhs_ipv$year))
sum(is.na(dhs_ipv$region))

## Suppression des valeurs manquantes
dhs_ipv <- na.omit(dhs_ipv)

## Statistiques descriptives
summary(dhs_ipv$beat_burnfood)
summary(dhs_ipv$beat_goesout)
summary(dhs_ipv$sec_school)
summary(dhs_ipv$no_media)

## Diagramme en moustache variable quantitative
boxplot(dhs_ipv$beat_burnfood, ylab= "beat_burnfood", col = "orangered", main="Boxplot of beat_burnfood", ylim=c(0,80))
boxplot(dhs_ipv$beat_goesout, ylab= "beat_goesout", col = "royalblue", main="Boxplot of beat_goesout")
boxplot(dhs_ipv$sec_school, ylab= "sec_school", col = "salmon", main="Boxplot sec_school", ylim=c(0,80))
boxplot(dhs_ipv$no_media, ylab= "no media", col = "seagreen1", main="Boxplot of no media")

## Diagramme en moustache variable qualitative
boxplot(dhs_ipv$beat_burnfood~dhs_ipv$region, xlab = "Region", ylab = "beat_burnfood", col="palevioletred")
boxplot(dhs_ipv$beat_goesout~dhs_ipv$region, xlab = "Region", ylab = "beat_goesout", col="violetred1")
boxplot(dhs_ipv$sec_school~dhs_ipv$region, xlab = "Region", ylab = "sec_school", col="slateblue")
boxplot(dhs_ipv$no_media~dhs_ipv$region, xlab = "Region", ylab = "no media", col="yellowgreen")

## Camemberg
pie(table(dhs_ipv$region), clockwise = TRUE, col = c("springgreen","slateblue2","deepskyblue","tan1"))

## ANOVA un facteur
summary(aov(dhs_ipv$beat_burnfood ~ dhs_ipv$region, data = dhs_ipv))
summary(aov(dhs_ipv$beat_goesout ~ dhs_ipv$region, data = dhs_ipv))
summary(aov(dhs_ipv$sec_school ~ dhs_ipv$region, data = dhs_ipv))
summary(aov(dhs_ipv$no_media ~ dhs_ipv$region, data = dhs_ipv))

## Test Shapiro-wilk
shapiro.test(aov(dhs_ipv$beat_burnfood ~ dhs_ipv$region, data = dhs_ipv)$residuals) #(H1)
shapiro.test(aov(dhs_ipv$beat_goesout ~ dhs_ipv$region, data = dhs_ipv)$residuals) #(H1)
shapiro.test(aov(dhs_ipv$sec_school ~ dhs_ipv$region, data = dhs_ipv)$residuals) #(H1)
shapiro.test(aov(dhs_ipv$no_media ~ dhs_ipv$region, data = dhs_ipv)$residuals) #(H0)

qqnorm(aov(dhs_ipv$beat_burnfood ~ dhs_ipv$region, data = dhs_ipv)$residuals)

## Test Barlett
bartlett.test(aov(dhs_ipv$beat_burnfood ~ dhs_ipv$region, data = dhs_ipv)$residuals~dhs_ipv$region, data = dhs_ipv) #(H1)
bartlett.test(aov(dhs_ipv$beat_goesout ~ dhs_ipv$region, data = dhs_ipv)$residuals~dhs_ipv$region, data = dhs_ipv) #(H1)
bartlett.test(aov(dhs_ipv$sec_school ~ dhs_ipv$region, data = dhs_ipv)$residuals~dhs_ipv$region, data = dhs_ipv) #(H1)
bartlett.test(aov(dhs_ipv$no_media ~ dhs_ipv$region, data = dhs_ipv)$residuals~dhs_ipv$region, data = dhs_ipv) #(H1)

### les hypotheses de normalite et de l'homostedasticite des residus n'etant pas respecte
### nous utilisons Krustal-Wallis qui est une alternative a ANOVA dans ce cas.

## Test Krustal-Wallis
kruskal.test(dhs_ipv$beat_burnfood~dhs_ipv$region, data = dhs_ipv) #(H1)
kruskal.test(dhs_ipv$beat_goesout~dhs_ipv$region, data = dhs_ipv) #(H1)
kruskal.test(dhs_ipv$sec_school~dhs_ipv$region, data = dhs_ipv) #(H1)
kruskal.test(dhs_ipv$no_media~dhs_ipv$region, data = dhs_ipv) #(H1)

library(dunn.test)
dunn.test(dhs_ipv$beat_burnfood, dhs_ipv$region, method = "bonferroni")
dunn.test(dhs_ipv$beat_goesout, dhs_ipv$region, method = "bonferroni")
dunn.test(dhs_ipv$sec_school, dhs_ipv$region, method = "bonferroni")
dunn.test(dhs_ipv$no_media, dhs_ipv$region, method = "bonferroni")
