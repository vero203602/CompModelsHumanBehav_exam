### Progetto Computational    ###
### Models of human behaviour ###


setwd("/Users/veronicacipriani/Desktop/Data Science/anno II/primo sem/computational models for human behaviour/progetto/codice R")
df <- read.csv('quartieri_e_numari.csv')

View(df)
# Correlation between n_poi and n_fermate
library(corrplot)
cor(df[,c(2, 3)])
corrplot.mixed(cor(df[,c(2, 3)]), upper="ellipse")

cor(df[,c(2, 4:19)])
corrplot.mixed(cor(df[,c(2, 4:19)]), upper="ellipse")

# Linear Regression
model <- lm(n_fermate ~ n_poi + Ristorante + Tempo.libero + 
              Parcheggio + Servizi + 
              Alimentari + Museo.monumento + 
              Istituzioni + Universita_e_altro, data=df)
summary(model)

#in order, i take away
# - Editoria
# - Sport
# - Farmacia
# - Biblioteca
# - Others

###
mean <- df[, 3]
mean
mean(mean)

bus <- df[, 2]
bus
mean(bus)

### Correlazione poi stops nei quartieri con piu poi

df_sub <- df[c(29, 30, 31, 42, 33, 23, 28, 38, 22, 13, 8),]
View(df_sub)

cor(df_sub[,c(2, 3)])
corrplot.mixed(cor(df_sub[,c(2, 3)]), upper="ellipse")



### Tolgo il centro, in quanto la maggior parte della zona non è percorribile
### da mezzi

df_no_centro <- df[-29, ]
View(df_no_centro)

cor(df_no_centro[,c(2, 3)])
corrplot.mixed(cor(df_no_centro[,c(2, 3)]), upper="ellipse")

cor(df_no_centro[,c(2, 4:19)])
corrplot.mixed(cor(df_no_centro[,c(2, 4:19)]), upper="ellipse")


model <- lm(n_fermate ~ n_poi + Ristorante + Tempo.libero + Hotels.camere+ 
              Parcheggio + Bar.vita.notturna + Servizi + 
              Alimentari + Museo.monumento + Istituzioni + Universita_e_altro, data=df_no_centro)
summary(model)

