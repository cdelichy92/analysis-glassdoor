library(ROCR)
library(reshape2)
library(ggplot2)
library(dplyr)


setwd("/Users/Louis/Desktop/Stanford/MS\&E\ 231/Project/API_results")

#load data
software_engineer <- read.table("software_engineer_API_clean.tsv",sep="\t", header=TRUE)
software_engineer <- software_engineer[software_engineer$Work.life.balance > 0.0,]

banking <- read.table("banking_API_clean.tsv", sep="\t",header=TRUE)
banking <- banking[banking$Work.life.balance > 0.0,]

aerospace <- read.table("aerospace_API _clean.tsv",sep="\t", header=TRUE)
aerospace <- aerospace[aerospace$Work.life.balance > 0.0,]

consulting <- read.table("consulting_API_clean.tsv",sep="\t", header=TRUE)
consulting <- consulting[consulting$Work.life.balance > 0.0,]

education <- read.table("education_API_clean.tsv",sep="\t", header=TRUE)
education <- education[education$Work.life.balance > 0.0,]

social <- read.table("social_API_clean.tsv",sep="\t", header=TRUE)
social <- social[social$Work.life.balance > 0.0,]

real_estate <- read.table("real_estate_API_clean.tsv",sep="\t", header=TRUE)
real_estate <- real_estate[real_estate$Work.life.balance > 0.0,]

travel <- read.table("travel_API_clean.tsv",sep="\t", header=TRUE)
travel <- travel[travel$Work.life.balance > 0.0,]

food <- read.table("food_API_clean.tsv",sep="\t", header=TRUE)
food <- food[food$Work.life.balance > 0.0,]

retail <- read.table("retail_API_clean.tsv",sep="\t", header=TRUE)
retail <- retail[retail$Work.life.balance > 0.0,]

entertainment <- read.table("entertainment_API_clean.tsv",sep="\t", header=TRUE)
entertainment <- entertainment[entertainment$Work.life.balance > 0.0,]

energy <- read.table("energy_API_clean.tsv",sep="\t", header=TRUE)
energy <- energy[energy$Work.life.balance > 0.0,]

oil <- read.table("oil_API_clean.tsv",sep="\t", header=TRUE)
oil <- oil[oil$Work.life.balance > 0.0,]

construction <- read.table("construction_API_clean.tsv",sep="\t", header=TRUE)
construction <- construction[construction$Work.life.balance > 0.0,]

pharmaceuticals <- read.table("pharmaceuticals_API_clean.tsv",sep="\t", header=TRUE)
pharmaceuticals <- pharmaceuticals[pharmaceuticals$Work.life.balance > 0.0,]

insurance <- read.table("insurance_API_clean.tsv",sep="\t", header=TRUE)
insurance <- insurance[insurance$Work.life.balance > 0.0,]

health <- read.table("health_API_clean.tsv",sep="\t", header=TRUE)
health <- health[health$Work.life.balance > 0.0,]

restaurants <- read.table("restaurants_API_clean.tsv",sep="\t", header=TRUE)
restaurants <- restaurants[restaurants$Work.life.balance > 0.0,]

data <- rbind(software_engineer,banking,aerospace,consulting,education,social,real_estate,travel,food,retail,entertainment,energy,oil,construction,pharmaceuticals,insurance,health,restaurants)
data <- data[!duplicated(data$Name), ]
data$Sector <- gsub("&amp;", "&", data$Sector)
data$Industry <- gsub("&amp;", "&", data$Industry)

sectors <- group_by(data, Sector)
sectors <- summarise(sectors,Count = n(),
                           Mean.Overall.Rating=mean(Overall.rating),Variance.Overall.Rating=var(Overall.rating),
                           Mean.Work.life.balance.Rating=mean(Work.life.balance),Variance.Work.life.balance.Rating=var(Work.life.balance),
                           Mean.Senior.Leadership.Rating=mean(Senior.Leadership),Variance.Senior.Leadership.Rating=var(Senior.Leadership),
                           Mean.Compensation.and.benefits.Rating=mean(Compensation.and.benefits),Variance.Compensation.and.benefits.Rating=var(Compensation.and.benefits),
                           Mean.Career.opportunities.Rating=mean(Career.opportunities),Variance.Career.opportunities.Rating=var(Career.opportunities),
                           Mean.Recommend.to.friend.Rating=mean(Recommend.to.friend),Variance.Recommend.to.friend.Rating=var(Recommend.to.friend)
                           )
sectors <- sectors[sectors$Count > 15,]

life_money_sector <- ggplot(sectors, aes(Mean.Work.life.balance.Rating,Mean.Compensation.and.benefits.Rating, label = Sector))+ geom_point(alpha = 0.5)+geom_text(aes(label=Sector),hjust=0, vjust=0)
life_money_sector

life_opportunity_sector <- ggplot(sectors, aes(Mean.Work.life.balance.Rating,Mean.Career.opportunities.Rating, label = Sector))+ geom_point(alpha = 0.5)+geom_text(aes(label=Sector),hjust=0, vjust=0)
life_opportunity_sector

industry <- group_by(data, Industry)
industry <- summarise(industry,Count = n(),
                      Mean.Overall.Rating=mean(Overall.rating),Variance.Overall.Rating=var(Overall.rating),
                      Mean.Work.life.balance.Rating=mean(Work.life.balance),Variance.Work.life.balance.Rating=var(Work.life.balance),
                      Mean.Senior.Leadership.Rating=mean(Senior.Leadership),Variance.Senior.Leadership.Rating=var(Senior.Leadership),
                      Mean.Compensation.and.benefits.Rating=mean(Compensation.and.benefits),Variance.Compensation.and.benefits.Rating=var(Compensation.and.benefits),
                      Mean.Career.opportunities.Rating=mean(Career.opportunities),Variance.Career.opportunities.Rating=var(Career.opportunities),
                      Mean.Recommend.to.friend.Rating=mean(Recommend.to.friend),Variance.Recommend.to.friend.Rating=var(Recommend.to.friend)
)
industry <- industry[industry$Count > 15,]

life_money_industry <- ggplot(industry, aes(Mean.Work.life.balance.Rating,Mean.Compensation.and.benefits.Rating, label = Industry , color = Industry))+ geom_point(alpha = 0.5)
life_money_industry <- direct.label(life_money_industry,list(cex=0.9,bumpup))
life_money_industry

