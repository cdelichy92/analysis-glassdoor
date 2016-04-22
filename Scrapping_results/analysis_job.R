library(ROCR)
library(reshape2)
library(ggplot2)
library(dplyr)


setwd("/Users/Louis/Desktop/Stanford/MSE231/Project/Scrapping_results")

#load data
data_scientist <- read.table("data_scientist.tsv",sep="\t", header=TRUE)
software_engineer <- read.table("software_engineer.tsv",sep="\t", header=TRUE)
senior_software_engineer <- read.table("senior_software_engineer.tsv",sep="\t", header=TRUE)
product_manager <- read.table("product_manager.tsv",sep="\t", header=TRUE)
designer <- read.table("designer.tsv",sep="\t", header=TRUE)

data <- merge(data_scientist,software_engineer,by="Company")
data <- merge(data,senior_software_engineer,by="Company")
data <- merge(data,product_manager,by="Company")

data <- merge(data,designer,by="Company")

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

