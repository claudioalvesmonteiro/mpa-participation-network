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
library(readr)


RQDA()


# importar base de conselheiros
insti <- read_csv("data/preprocessed/consel_instituicoes.csv")

# function to standardize string
cleanString <- function(string){
  string_clean <- str_replace_all(string, ' ', '_')%>%
    str_replace_all( '-', '')%>%
    str_replace_all( '/', '_')%>%
    stri_trans_general("latin-ascii")%>%
    tolower()
}

insti$codename <- cleanString(paste0(insti$nome_consel,'_',insti$entidade_sigla))
cont_cod_data$codename <- cleanString(cont_cod_data$Var1)

###########


# visualizar a contagem de cada codigo
sumario_cod <- summaryCodings()
cont_cod_data <- data.frame(sumario_cod$NumOfCoding)

# merge to verify
cont_insti = merge(cont_cod_data, insti, by='codename', all.x = T)
write.csv(cont_insti[,c(1,3,4)], 'cont_output_rqda.csv', row.names = F)


###########

# visualizar infos sobre cada codificacao
coding_table <- getCodingTable()

# clean string
coding_table$codename <- cleanString(coding_table$codename)

# merge
coding_table_final <- merge(coding_table, insti, by='codename')

# export 
write.csv(coding_table_final, 'data/preprocessed/council_table.csv', row.names = F)

# select conflict and cooperation and save
conflict_coop = coding_table[coding_table$codename == 't_cat_conflito' | coding_table$codename == 't_cat_cooperacao',]
write.csv(conflict_coop, 'data/preprocessed/conflict_coop_table.csv', row.names = F)
