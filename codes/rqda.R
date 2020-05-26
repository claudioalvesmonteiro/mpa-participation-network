#=======================================
# paper marine policy
#
#
#========================================


# load package
library(RQDA)

# visualizar a contagem de cada codigo
sumario_cod <- summaryCodings()

# contagem de cada codigo
cont_cod_data <- data.frame(sumario_cod$NumOfCoding)

# visualizar infos sobre cada codificacao
coding_table <- getCodingTable()

# export 
write.csv('data/',coding_table, row.names = F)
