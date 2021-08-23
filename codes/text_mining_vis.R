# Load
library("wordcloud")
library("RColorBrewer")
require(readr)
library(ggpubr)

df = read_csv('data/words_full.csv')

#df = df[-c(1,3,8,12,14,21,27),]


w = wordcloud(words = df$word, freq = df$freq, min.freq = 1,
          max.words=25, random.order=FALSE, #rot.per=0.35, 
          colors=brewer.pal(8, "Dark2"), scale=c(4,.5))

ggsave("wordcloud_full.png", w, path = "results", width = 7, height = 7, units = "in")

#------------------------------
# by year
#------------------------------

df = read_csv('data/words_by_year.csv')

library(ggplot2)
library(viridis)
library(hrbrthemes)

anofunc <- function(data, year){
  
  # selecionar ano e ordenar
  ano = df[df$Ano == year,]
  ano$word <- factor(ano$word, levels = ano$word[order(ano$freq)])
  
  # Graph
  plot = ggplot(ano, aes(y=word, x=freq)) + 
    geom_bar(position="dodge", stat="identity") +
    scale_fill_viridis(discrete = T, option = "E") +
    ggtitle(as.character(year)) +
    theme_minimal() +
    theme(legend.position="none") +
    xlab("Freq")+
    ylab("")
  
  return(plot)
}


ano11 = anofunc(df, 2011)
ano12 = anofunc(df, 2012)
ano13 = anofunc(df, 2013)
ano14 = anofunc(df, 2014)
ano15 = anofunc(df, 2015)
ano16 = anofunc(df, 2016)
ano17 = anofunc(df, 2017)
ano18 = anofunc(df, 2018)
ano19 = anofunc(df, 2019)
ano20 = anofunc(df, 2020)


ggarrange(ano11, ano12, ano13, ano14, ano15,
          ano16, ano17, ano18, ano19, ano20)

ggsave("wordcloud_by_year.png", path = "results", width = 8, height = 10, units = "in")
