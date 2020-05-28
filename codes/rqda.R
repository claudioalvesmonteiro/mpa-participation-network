#=======================================
# paper marine policy
# claudio monteiro & beatriz mesquita
#
# @claudioalvesmonteiro 2020
#========================================


# load packages
library(readxl)
library(RQDA)
library(stringr)
library(stringi)
library(dplyr)

# 
RQDA()

# visualizar a contagem de cada codigo
sumario_cod <- summaryCodings()

# contagem de cada codigo
cont_cod_data <- data.frame(sumario_cod$NumOfCoding)

# visualizar infos sobre cada codificacao
coding_table <- getCodingTable()

# importar base de conselheiros
insti <- read_excel("data/preprocessed/APA_instituicoes.xlsx")

# preprocess names to merge
insti$codename <- paste0(insti$nome_consel,'_',insti$entidade_sigla)
insti$codename <- str_replace_all(insti$codename, ' ', '_')%>%
                          stri_trans_general("latin-ascii")%>%
                          tolower()
  
coding_table$codename <- stri_trans_general(coding_table$codename, "latin-ascii")%>%
                       tolower()


# merge
coding_tablex <- merge(coding_table, insti, by='codename')

# export 
write.csv(coding_tablex, 'data/preprocessed/council_table.csv', row.names = F)

# select conflict and cooperation and save
coding_tabley = coding_table[coding_table$codename == 't_cat_conflito' | coding_table$codename == 't_cat_cooperacao',]
write.csv(coding_tabley, 'data/preprocessed/conflict_table.csv', row.names = F)
