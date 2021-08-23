

# import packages
import pandas as pd
import nltk
from os import listdir
import unidecode


#-----------------------
# get text data
#-----------------------

# get text path
list_text = listdir('data/text')

# get text by meeting
data = {'meeting':[], 'original_text':[]}
for i in list_text:
    try:
        text = open('data/text/'+i,  encoding="Latin-1").read()
        text = text.replace('\x00', '')
        data['meeting'].append(i[:-4])
        data['original_text'].append(text)
    except:
        print(i, 'unsucessful')

data = pd.DataFrame(data)

# BY ANO
data['Ano'] = 0000
data['Ano'][(data.meeting == 'meeting_1') | (data.meeting == 'meeting_2') | (data.meeting == 'meeting_3')] = 2011
data['Ano'][(data.meeting == 'meeting_4') | (data.meeting == 'meeting_5')] = 2012
data['Ano'][(data.meeting == 'meeting_6') | (data.meeting == 'meeting_7') | (data.meeting == 'meeting_8') | (data.meeting == 'meeting_9')] = 2013
data['Ano'][(data.meeting == 'meeting_10') | (data.meeting == 'meeting_11') | (data.meeting == 'meeting_12') | (data.meeting == 'meeting_13')] = 2014
data['Ano'][ (data.meeting == 'meeting_14') | (data.meeting == 'meeting_15') | (data.meeting == 'meeting_16') | (data.meeting == 'meeting_17') ] = 2015
data['Ano'][(data.meeting == 'meeting_18') | (data.meeting == 'meeting_19') | (data.meeting == 'meeting_20')  | (data.meeting == 'meeting_21') ] = 2016
data['Ano'][(data.meeting == 'meeting_22') | (data.meeting == 'meeting_23') | (data.meeting == 'meeting_24')  ] = 2017
data['Ano'][(data.meeting == 'meeting_25') | (data.meeting == 'meeting_26') | (data.meeting == 'meeting_27')  ] = 2018
data['Ano'][(data.meeting == 'meeting_28') | (data.meeting == 'meeting_29') | (data.meeting == 'meeting_30') | (data.meeting == 'meeting_31') | (data.meeting == 'meeting_32') ] = 2019
data['Ano'][(data.meeting == 'meeting_33') | (data.meeting == 'meeting_34') | (data.meeting == 'meeting_35') ] = 2020


# get full text  ##
#data = ''
#for i in list_text:
#    try:
#        text = open('data/text/'+i,  encoding="Latin-1").read()
#        text = text.replace('\x00', '')
#        data += text+' '
#    except:
#        print(i, 'unsucessful')

#---------------
# clean text
#---------------

def cleanTextToken(text, lemma = False):
    ''' standardize text to extract words
    '''
    # remove accents
    text = unidecode.unidecode(text)
    # text to lowercase
    text = text.lower()
    # remove numbers
    text = ''.join([i for i in text if not i.isdigit()]) 
    # remove punctuation
    from nltk.tokenize import RegexpTokenizer
    tokenizer = RegexpTokenizer(r'\w+') # preserve words and alphanumeric
    text = tokenizer.tokenize(text)
    # remove stopwords
    from nltk.corpus import stopwords
    stop = set(stopwords.words('portuguese'))
    text = [w for w in text if not w in stop] 
    # remove text
    unwanted = ['paulo','cac','ima','sobre','nenhum','disse','gestapso','nao', 'sao', 'ser', 'b', 'c', 'ja', 'napso', 'reuniapso', 'm', 'al', 'ria', 's']
    text = list(filter(lambda a: a not in unwanted, text))
    # lemmatization
    if lemma:
        from nltk.stem import WordNetLemmatizer 
        lemmatizer = WordNetLemmatizer() 
        text = [lemmatizer.lemmatize(word) for word in text]
    # return clean token
    return(text)

# run cleaning
#preprocessed_text = []
#for i in range(len(data)):
#    preprocessed_text.append(cleanTextToken(data['original_text'][i]))
#data['preprocessed_text'] = preprocessed_text

# run cleaning year
preprocessed_data = {'Ano':[], 'preprocessed_text':[]}
for i in data['Ano'].unique():
    ano = data[data.Ano == i]
    ano_texto=''
    for anotxt in ano['original_text']:
        ano_texto += anotxt+' '
    preprocessed_data['preprocessed_text'].append(cleanTextToken(ano_texto))
    preprocessed_data['Ano'].append(i)

preprocessed_data = pd.DataFrame(preprocessed_data)

#data =  cleanTextToken(data) ##

#---------------------
# count words
#---------------------

# count function
def wordCount(txt_list):
    ''' count frequency of words in tokenized list
        and save in dataframe
    '''
    wordfreq = {'word':[],'freq':[]}
    for word in txt_list:
        if word not in wordfreq['word']:
            wordfreq['word'].append(word)                   # save word
            wordfreq['freq'].append(txt_list.count(word))   # save freq
    count = pd.DataFrame(wordfreq)
    # sort_values in df
    count.sort_values('freq', inplace=True, ascending=False)
    return count

# run counting for each meeting
#count_data = pd.DataFrame({'word':[],'freq':[], 'meeting':[]})
#for i in range(len(data)):
#    words = wordCount(data['preprocessed_text'][i])
#    words['meeting'] = data['meeting'][i]
#    count_data = pd.concat([words, count_data])

# run counting for each year
count_data = pd.DataFrame({'word':[],'freq':[], 'Ano':[]})
for i in range(len(preprocessed_data)):
    words = wordCount(preprocessed_data['preprocessed_text'][i])[0:10]
    words['Ano'] = preprocessed_data['Ano'][i]
    count_data = pd.concat([words, count_data])

data = wordCount(data) ##
data[0:25].to_csv('data/words_full.csv', index=False)

# salvar
count_data.to_csv('data/words_by_year.csv', index=False)

#============================
# sentiment analysis
#============================



def ruledSentimentTextAgg(token_list, category, rule='near'):
    ''' aggregate text in token list based on rules:
        all - agg all tokens in list
        next - agg tokens next to the word
        near - agg tokens 3 words far from category word
     '''
    text = ''
    for i in range(len(token_list)):
        if category in token_list[i]:
            row = token_list[i]
            cat_index = row.index(category)
            if rule == 'all':
                for word in row:
                    text = text + word + ' '  
            if rule == 'next':
                if cat_index > 0:
                    text += row[cat_index-1] + ' '
                if cat_index < (len(row)-1):
                    text += row[cat_index+1] + ' '
            if rule == 'near':
                count_id = 0
                while count_id < 3:
                    try:
                        word = row[cat_index+count_id]
                        if nltk.pos_tag([word])[0][1] == 'JJ':
                            text += word + ' '
                    except:
                        pass
                    count_id += 1
                count_id = 0    
                while count_id > -3:
                    try:
                        word = row[cat_index+count_id]
                        if nltk.pos_tag([word])[0][1] == 'JJ':
                            text += word + ' '
                    except:
                        pass
                    count_id -= 1
    return text