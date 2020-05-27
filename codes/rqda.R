#=======================================
# paper marine policy
#
#
#========================================


# load packages
library(readxl)
library(RQDA)
library(stringr)
library(stringi)
library(dplyr)

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
  
coding_table

# combinar com base de codificacoes

# export 
write.csv(coding_table, 'data/preprocessed/coding_table.csv', row.names = F)
