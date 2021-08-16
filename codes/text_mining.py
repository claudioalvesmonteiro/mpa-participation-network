
# import packages
import pandas as pd
import nltk
from wordcloud import WordCloud
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
    # lemmatization
    if lemma:
        from nltk.stem import WordNetLemmatizer 
        lemmatizer = WordNetLemmatizer() 
        text = [lemmatizer.lemmatize(word) for word in text]
    # return clean token
    return(text)

# run cleaning
preprocessed_text = []
for i in range(len(data)):
    preprocessed_text.append(cleanTextToken(data['original_text'][i]))

data['preprocessed_text'] = preprocessed_text

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

# run counting
count_data = pd.DataFrame({'word':[],'freq':[], 'meeting':[]})
for i in range(len(data)):
    words = wordCount(data['preprocessed_text'][i])
    words['meeting'] = data['meeting'][i]
    count_data = pd.concat([words, count_data])

#data = wordCount(data) ##
#data.to_csv('data/words_full.csv', index=False)

# salvar
count_data.to_csv('data/words_by_meeting.csv', index=False)

