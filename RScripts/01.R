library(ggplot2)
library(plotly)

df = read.delim('/home/sean/NERCflora/formFinal/finalFlat.csv', sep='|', na.strings=c("","NA","nan", "NaN", "Na"))

df$myFert5 <- factor(df$myFert5, levels = c("selfing", "normally self", "mixed", "normally cross", "outcrossing"))
df$myFert3 <- factor(df$myFert3, levels = c("selfing", "mixed", "outcrossing"))
df$myHeavyMet <- factor(df$myHeavyMet, levels = c("none", "pseudometallophyte", "local metallophyte", "absolute metallophyte"))
df$myRarityCombined <- factor(df$myRarityCombined, levels = c("x", "r", "o", "s", "n"))

fert3VheavyMet.df = as.data.frame(table(df$myFert3, df$myHeavyMet))
fert5VheavyMet.df = as.data.frame(table(df$myFert5, df$myHeavyMet))

p1 = ggplot(fert3VheavyMet.df, aes(x=fert3, y=heavyMet)) +
  geom_tile(aes(fill = Freq)) +
  scale_fill_distiller(palette = "YlGnBu") +
  labs(title = "Heatmap of Fertilization_Mode_3 vs. Heavy_Metal_Resistance")

p2 = ggplot(fert5VheavyMet.df, aes(x=fert5, y=heavyMet)) +
  geom_tile(aes(fill = Freq)) +
  scale_fill_distiller(palette = "YlGnBu") +
  labs(title = "Heatmap of Fertilization_Mode_5 vs. Heavy_Metal_Resistance")



lm3VMet = lm(as.numeric(df$myHeavyMet) ~ as.numeric(df$myFert3))

lm5VRange = lm(df$myPlantAtRange ~ as.numeric(df$myFert5))
aov5VRange = aov(df$myPlantAtRange ~ myFert5, data=df)
aov3VRange = aov(df$myPlantAtRange ~ myFert3, data=df)

df %>% filter(!is.na(myFert3)) %>% filter(!is.na(myPlantAtRange)) %>% ggplot(aes(x=myFert3, y=myPlantAtRange)) + geom_boxplot()
df %>% filter(!is.na(myFert5)) %>% filter(!is.na(myPlantAtRange)) %>% ggplot(aes(x=myFert5, y=myPlantAtRange)) + geom_boxplot()

f = as.formula(myFert5 ~ Petal.no + Mono.poly.carpic +
                 + myEBergL + myEBergF + myEBergR+ myEBergN+ myEBergS
               + myPlantAtNativeStatus + myPlantAtConservationStatus
               + myPlantAtChangeIndex + myPlantAtHeight
               + myPlantAtPern1 + myPlantAtPern2 + myPlantAtLife1+ myPlantAtLife2
               + myPlantAtWood + myPlantAtClone1
               + myPlantAtMajorBiome + myPlantAtEastLim
               + myPlantAtTjan + myPlantAtTjul + myPlantAtPrecip)

tree3 = tree(f, df)


pairVals<-function(series, val1, val2){
  serRet <- series
  serRet[!(serRet==val1 | serRet==val2)] <- NaN
  return(serRet)
}
wilcox.test(df$myPlantAtRange ~ pairVals(df$myFert3, 'selfing', 'mixed'))

ggplot(df, aes(x=myPlantAtRange)) + geom_density()

rangeRarityFilt = filter(df, !(is.na(df$myRarityCombined) | is.na(df$myPlantAtRange) | is.na(df$myFert5)))
model <- lm(as.numeric(myFert5)~myPlantAtRange+as.numeric(myRarityCombined), data=rangeRarityFilt)
res <- resid(model)
