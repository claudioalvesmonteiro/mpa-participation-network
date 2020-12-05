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
library(ggplot2)


RQDA()



#==================================#
# CAPTURA DOS DADOS DA CODIFICACAO

# visualizar a contagem de cada codigo
sumario_cod <- summaryCodings()

# contagem de cada codigo
cont_cod_data <- data.frame(sumario_cod$NumOfCoding)

# visualizar infos sobre cada codificacao
coding_table <- getCodingTable()

#================================#
# Analise dos temas em debate    #
#================================# 

# selecionar contagem de temas

# criar variavel 'tema' no banco 'cont_cod_data'
cont_cod_data <- mutate(cont_cod_data, tema = 0)

# detectar termo 'tema_' na varivael 'Var1' e atribuir valor 1 a variavel 'tema'
cont_cod_data$tema[str_detect(cont_cod_data$Var1, "tema_")] <- 1

# selecionar os casos em que tema = 1
cont_cod_tema <- cont_cod_data[cont_cod_data$tema == 1,]

# calcular proporcao e arredondar
cont_cod_tema <- mutate(cont_cod_tema, prop_tema = (Freq / sum(Freq))*100 )

# criar variavel de prop com "%" 
cont_cod_tema$prop_tema2 <- paste(round(cont_cod_tema$prop_tema, 2), "%", sep="")

# criar uma nova variavel com nomes dos temas
cont_cod_tema <- mutate(cont_cod_tema, nomes_temas = Var1)
cont_cod_tema$nomes_temas <- c('Conselho',"Educação Socioambiental", "Fiscalização e Monitoramento", "Gestão APACC", 
                                "Plano de Manejo", 'Recuperação e Biodiversidade',"Recursos Financeiros", "Zoneamento")


# ordenar
cont_cod_tema$nomes_temas <- factor(cont_cod_tema$nomes_temas, 
                                    levels = cont_cod_tema$nomes_temas[order(cont_cod_tema$prop_tema)])

# visualizar graficamente e salvar
ggplot(cont_cod_tema, aes(x = nomes_temas, y = prop_tema))+
  geom_bar(stat = "identity", fill = "#15041c") +
  geom_label(aes(x = nomes_temas, y = prop_tema, label = prop_tema2), size = 2.3)+
  labs(y = "Procentagem do Total", x = "", title = "") +
  coord_flip()

ggsave("prop_debate_tema.png", path = "results", width = 7, height = 3, units = "in")

#======================================#
#     ANALISE DE VOZ NOS DEBATES       #
#======================================#

#======== tratar dados =========#

# selecionar codigos dos representantes
paste_voz<- c("cat_", "tema_", "DESTAQUES", "DUVIDA_", "atua_", "DECISOES", "termo_", "tema2_")
cont_cod_data <- mutate(cont_cod_data, select_voz = 1)
cont_cod_data$select_voz[str_detect(cont_cod_data$Var1, paste(paste_voz, collapse = '|'))] <- 2

codes_represent <- cont_cod_data[cont_cod_data$select_voz == 1,]

# importar base de instituicoes por representante
<<<<<<< HEAD
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
codes_represent$codename <- cleanString(codes_represent$Var1)


# mergir base de conselheiros
data_consel <- merge(insti, codes_represent, by = "codename", all.y = T)


#===== ANALISE CATEGORIA 1 =====#

# remover gestores ICMBio

base_rep_sem_icmbio <- data_consel[data_consel$entidade_sigla != "ICMBIO",]
dataGrupo <- aggregate(base_rep_sem_icmbio$Freq, by=list(grupo_setorial=base_rep_sem_icmbio$categoria1), FUN=sum)



#---- inserir info de assentos ----#
# http://www.icmbio.gov.br/apacostadoscorais/images/stories/conapac/Mem%C3%B3ria_18_reuni%C3%A3o_aprovada.pdf


dataGrupo$numero_assento <- c(2, 6, 6, 12, 8, 3, 3) 

dataGrupo <- mutate(dataGrupo, prop_assento = (round(((x/numero_assento)), 1)) )

# proporcao em relacao ao total
dataGrupo <- mutate(dataGrupo, proporcao_total = round(((x / sum(x))*100),1) )
dataGrupo <- mutate(dataGrupo, proporcao_total_label = paste0(proporcao_total,"%") )

# renomear categoria 6

#dataGrupo$grupo_setorial[6] <- "Organizações de Educação, Cultura  \n  e Associações Comunitárias"

# renomear variavel
colnames(dataGrupo)[2] <- "situacoes_de_fala"
dataGrupo$UC <- "APA Costa dos Corais"


dataGrupo$sector_group = c('Agriculture and Industry', 'Fishery', 'Tourism', 'Public Government', 'Research Institutions', 'Environmental NGOs', 'Local Associations')

# ordenar
dataGrupo$sector_group <- factor(dataGrupo$sector_group, levels = dataGrupo$sector_group[order(dataGrupo$prop_assento)])


#inserir categorias
dataGrupo$categoria_inst <- c("Sociedade Civil", "Sociedade Civil","Poder Público", "Poder Público",
                              "Sociedade Civil", "Sociedade Civil", "Sociedade Civil")

# salvar

write.csv(dataGrupo, "results/apa_fala_data.csv", row.names = F)


ggplot(dataGrupo, aes(x = sector_group, y = prop_assento ))+
  geom_bar(stat = "identity") +
  geom_label(aes( label = prop_assento ), size = 2.5)+
  labs(y = "Participation Index", x = "", title = "") +
  coord_flip()+
  theme_minimal()%+replace% 
  theme(legend.position="bottom")

ggsave("prop_voz_cat.png", path = "results", width = 8, height = 3, units = "in")



dataGrupo$sector_group <- factor(dataGrupo$sector_group, levels = dataGrupo$sector_group[order(dataGrupo$proporcao_total)])

ggplot(dataGrupo, aes(x = sector_group, y = proporcao_total ))+
  geom_bar(stat = "identity") +
  geom_label(aes(label = proporcao_total ), size = 2.5)+
  labs(y = "Total Participation", x = "", title = "") +
  coord_flip()+
  theme_minimal()%+replace% 
  theme(legend.position="bottom")
ggsave("total_voz_cat.png", path = "results", width = 8, height = 3, units = "in")

write.csv(dataGrupo, "resultados/tabelas/apa_fala_data.csv", row.names = F)


#===== ANALISE CATEGORIA 2 =====#

# contar
count_cat2 <- aggregate(base_representantes$Freq, by=list(Category=base_representantes$categoria2), FUN=sum)

# sem os gestores
count_cat2 <- aggregate(base_rep_sem_icmbio$Freq, by=list(Category=base_rep_sem_icmbio$categoria2), FUN=sum)

# transformar em prop e ordenar
count_cat2 <- mutate(count_cat2, prop_cat2 = (x / sum(x))*100 )
count_cat2$prop_cat2 <- round(count_cat2$prop_cat2, 2)
count_cat2$Category <- factor(count_cat2$Category, 
                              levels = count_cat2$Category[order(count_cat2$prop_cat2)])
count_cat2$prop_cat2.2 <- paste(round(count_cat2$prop_cat2, 2), "%", sep="")

# ggplot2
ggplot(count_cat2, aes(x = Category, y = prop_cat2))+
  geom_bar(stat = "identity", fill = "#15041c") +
  geom_label(aes(x = Category, y = prop_cat2, label = prop_cat2.2), size = 3.2)+
  labs(y = "Porcentagem", x = "", title = "") +
  coord_flip()
ggsave("prop_voz_cat2.png", path = "Resultados",width = 8, height = 3, units = "in")

