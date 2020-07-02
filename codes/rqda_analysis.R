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

# function to standardize string
cleanString <- function(string){
  string_clean <- str_replace_all(string, ' ', '_')%>%
    str_replace_all( '-', '')%>%
    str_replace_all( '/', '_')%>%
    stri_trans_general("latin-ascii")%>%
    tolower()
}

insti$codename <- paste0(insti$nome_consel,'_',insti$entidade_sigla)
insti <- data.frame(sapply(insti, function(x) cleanString(x)))
coding_table$codename <- cleanString(coding_table$codename)

# merge
counselors <- merge(coding_table, insti, by='codename')

# export 
write.csv(counselors, 'data/preprocessed/council_table.csv', row.names = F)

# select conflict and cooperation and save
conflict_coop = coding_table[coding_table$codename == 't_cat_conflito' | coding_table$codename == 't_cat_cooperacao',]
write.csv(conflict_coop, 'data/preprocessed/conflict_table.csv', row.names = F)
