'''
paper marine policy
claudio monteiro & beatriz mesquita

@claudioalvesmonteiro 2020
'''

# https://python-graph-gallery.com/325-map-colour-to-the-edges-of-a-network/


# import packages
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# import data
counselor_data = pd.read_csv('data/preprocessed/council_table.csv', sep=',', encoding='latin1')
category_data = pd.read_csv('data/preprocessed/conflict_coop_table.csv')

#===========================
# preprocessing
#===========================

# remove goverment workers from APACC management

counselor_data = counselor_data[counselor_data['entidade_sigla']!='ICMBIO']



#========================================
# functions to build network dataframe
#======================================

def combinationDict(categories, n_combination):
    ''' generate possible combinations of categories 
       as dictionary
    '''
    # generate combinations
    import itertools
    combinations = itertools.combinations(categories, n_combination)
    # append combinations to list 
    data_dict={'net_from':[], 'net_to':[], 'count':[], 'level':[]}
    for i in combinations:
        data_dict['net_from'].append(i[0])
        data_dict['net_to'].append(i[1])
    # set range os cont and level
    # level_ - sum n of appearances of both sectors [from_, to_] in the specific debate they were involved
    # count_ - append 1 for each situation that both sectors were involved
    data_dict['count'] = [0]*len(data_dict['net_to'])
    data_dict['level'] = [0]*len(data_dict['net_to'])
    # return data
    return data_dict



def searchAssociation(category, category_info, counselor_info, combinations):
    ''' function to measure the degree of association between sectors
        based on speech situations in debates of classified as #category
    '''
    # select data from category
    category_info =  category_info[category_info.codename == category]
    # select meeting
    for meet in category_data.filename.unique():
        meet_data = category_info[category_info.filename == meet].reset_index()
        counselor_data = counselor_info[counselor_info.filename == meet].reset_index()
        # loop on each coding inside meet
        for coding in range(len(meet_data)):
            range_meet = [*range(meet_data.index1[coding], meet_data.index2[coding]+1, 1)]
            coding_count = {}
            # loop on each counselor code inside meet and verify which sectors are involved in the debate
            for speech in range(len(counselor_data)):
                range_counselor = [*range(counselor_data.index1[speech], counselor_data.index2[speech]+1, 1)]
                prop_inside = isInThreshold(range_counselor, range_meet)
                if prop_inside > 0.9: # >90% match on text to allow codification error
                    cat_inside = counselor_data.categoria1[speech]
                    if cat_inside in coding_count:
                        coding_count[cat_inside] = coding_count[cat_inside] + 1
                    else:
                        coding_count[cat_inside] = 1
            # APPEND INFO TO DATABASE
            if coding_count:                
                for i in range(len(combinations['net_to'])):
                    if combinations['net_from'][i] in coding_count and combinations['net_to'][i] in coding_count:
                        combinations['level'][i] += coding_count[combinations['net_from'][i]] + coding_count[combinations['net_to'][i]]
                        combinations['count'][i] = combinations['count'][i] + 1
    return combinations

def isInThreshold(list_x, list_y):
    ''' function to count how much of a list is
        inside other list, return interpolation 
        degree of list_x to list_y
    '''
    prop_inside = []
    for i in list_x:
        if i in list_y:
            prop_inside.append(True)
    return sum(prop_inside)/len(list_x)

#=========================
# network visualization
#=======================

# create dictionary of possible pairs among categories
combinations = combinationDict(counselor_data.categoria1.unique(), 2)

# execute search 
combination_results = searchAssociation('t_cat_cooperacao', category_data, counselor_data, combinations)

# Build a dataframe with your connections
combination_results = pd.DataFrame(combination_results)

def rename_(col):
    col[col == 'Gestão Pública'] = 'Public Gov'
    col[col == 'ONGs Ambientalistas'] = 'Environmental NGOs'
    col[col == 'Agricultura, Indústria e Comércio'] = 'Agriculture and Industry'
    col[col == 'Atividade Pesqueira'] = 'Fishery'
    col[col == 'Atividade Turística'] = 'Tourism'
    col[col == 'Instituição de Ensino e Pesquisa'] = 'Research Inst.'
    col[col == 'Organizações de educação e cultura e associações comunitárias'] = 'Local Associations'
    return col

combination_results['net_from'] = rename_(combination_results['net_from'])
combination_results['net_to'] = rename_(combination_results['net_to'])

# filter out 'local associations' and 'agriculture and industry'
combination_results = combination_results[(combination_results.net_from != 'Local Associations') & (combination_results.net_from != 'Agriculture and Industry')]
combination_results = combination_results[(combination_results.net_to != 'Local Associations') & (combination_results.net_to != 'Agriculture and Industry')]

combination_results.sort_values('level', ascending=False)

# Build your graph
G = nx.from_pandas_edgelist(combination_results, 'net_from', 'net_to', create_using=nx.Graph() )
    
# Custom the nodes:
nx.draw(G, with_labels=True, 
            node_color='skyblue', 
            node_size=2000,
            edge_color=combination_results['level'], 
            width=5.0, edge_cmap=plt.get_cmap('Blues_r'))

# show
plt.show()