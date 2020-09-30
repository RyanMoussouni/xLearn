#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 14:45:03 2019
@author: xlearn
"""


#%% Packages
import numpy as np
import matplotlib.pyplot as plt
from anytree import Node,RenderTree
import time
import json
        
#%% Ontology building
class Internal_Ontology():
    '''
    Desc. Internal Ontology contient la liste des métier, compétences sous compétences (L), la liste des compétences, et des noeuds...
    '''
    def __init__(self, onet_cache=None, manual_build=True):
        super().__init__()
        self.is_built = False
        self.path = 'data_clean.json'
        self.IO_generator = iter(self.stream_read_json(self.path))
        self.name = 'Internal_Ontology'
        self.L=[]
        self.competences=[]
        self.sous_competences=[]
        self.root=Node("Competency Tree")
        self.competency_nodes=[]
        self._build() #builds the ontology from the database
        
    def _build(self):
        if not self.is_built:
            IO_generator = self.IO_generator
            L=self.L
            k=0
            while True:
                try:
                    elt=next(IO_generator)
                    triplet = [elt['Métier'],elt['Compétence'],elt['Sous-compétences']] 
                    if triplet[1] not in self.competences:
                        self.competency_nodes.append(Node(triplet[1],parent=self.root))
                    Node(triplet[2],parent=self.competency_nodes[-1])                    
                    self.competences.append(triplet[1])
                    self.sous_competences.append(triplet[2])
                    if len(L)>0:                        
                        dernier_element=L.pop()
                        if dernier_element[0]==triplet[0]:
                            #pdb.set_trace()
                            if elt['Compétence'] in dernier_element[1][0]:
                                dernier_element[1][1][k].append(triplet[2])
                            else:
                                dernier_element[1][0].append(triplet[1])
                                dernier_element[1][1].append([triplet[2]])
                                k+=1
                            L.append(dernier_element)
                        else:
                                L.append(dernier_element)
                                L.append([triplet[0],[[triplet[1]],[[triplet[2]]]]])
                                k=0
                        
                    else:
                       L.append([[elt['Métier']],[elt['Compétence'],[[elt['Sous-compétences']]]]])
                   
                except StopIteration:
                    break
        else:
            print('Ontology already built')
            

    def stream_read_json(self,path):
        ''' 
        Desc. To read the data as a stream
        '''
        start_pos = 0
        with open(self.path, 'r', encoding='utf-8') as f:
            obj = list(json.load(f))
            for i in range(len(obj)):
                try:
                    yield obj[i]
    
                except json.JSONDecodeError as e:
                    f.seek(start_pos)
                    json_str = f.read(e.pos)
                    obj = json.loads(json_str)
                    start_pos += e.pos
                    yield obj[i]
            return

    def RenderTheTree(self):
        '''
        Desc. Show the tree of competencies
        '''
         for pre, fill, node in RenderTree(self.root):
             print("%s%s" % (pre, node.name))
             
    def RenderNode(self,Competence :str):
         Nodd= "Node('/Competency Tree/"+Competence+"')"
         strcomp=[str(value) for value in self.competency_nodes]
         index_Nodd=strcomp.index(Nodd)
         Noeud = self.competency_nodes[index_Nodd]
         for pre, fill, node in RenderTree(Noeud):
             print("%s%s" % (pre, node.name))


def distance_console(job_1 :str,job_2 :str, affichage_Competence=False):
    '''
    Desc. Afficher rapidement la distance entre deux métiers sur la console
    '''
    ontology = Internal_Ontology()
    G,frequency_list=frequence(ontology, show=False, return_frequency_list=True)
    distance(ontology.L, job_1, job_2, G, frequency_list, affichage_Competence)
    return

def distance(L :list,Job_1 :str, Job_2 :str, M :list, frequency_list :list, Affichage_Comp=False):
    '''
    Desc .Donne la distance entre un métier 1 et un métier 2
    '''
    score = 0
    competency_match=0
    subcomptency_match=0
    total = 0
    comp_communes=[]
    frequ_communes=[]
    sous_comp_communes=[]
    cluster_comp=[]
    cluster_nodes=[]
    str_cluster_nodes=[]
    for c,value  in enumerate(L):
        if value[0] == Job_1:
            c1=c
        if value[0]== Job_2:
            c2=c
    for value in L[c1][1][0]:
        frequency_value=frequency_list[M.index(value)]
        if value in L[c2][1][0]:            
            comp_communes.append(value)
            frequ_communes.append(frequency_value)
            competency_match+=1
            score += frequency_value #On dit qu'une compétence ça compte pour 1
        total += frequency_value
    for k in range(len(L[c1][1][1])):
        for value1 in L[c1][1][1][k]:
            comp=L[c2][1][0]
            
            for l in range(len(L[c2][1][1])):
                if value1 in L[c2][1][1][l]:
                    try:
                        sous_comp_communes.append([value1,comp[l]])
                        subcomptency_match+=1
                        #Une sous competence, ça compte pour 1
                    except IndexError:
                        print(L[c2][0],L[c1][0])
                    
        
    for value2 in sous_comp_communes:
        if value2[1] in comp_communes:
            cluster_comp.append(value2)
            
    if len(cluster_comp)>0:
        root=Node("Cluster")
        for value3 in cluster_comp:
            Nodd="Node("+value3[1]+",parent = root)"
            if Nodd in str_cluster_nodes:
                try:
                    index_node=str_cluster_nodes.index(Nodd)
                    Node(value3[0],parent=cluster_nodes[index_node][1])
                except ValueError:
                    print('une erreur')
            else:
                try:
                    cluster_nodes.append([value3[1],Node(value3[1],parent = root)])
                    str_cluster_nodes.append("Node("+value3[1]+",parent = root)")
                    Node(value3[0],parent=cluster_nodes[-1][1])
                except ValueError:
                    print('une erreur')
        for value in cluster_comp:
            competency = value[1]
            index_comp_fr= comp_communes.index(competency)
            frequency_value= frequ_communes[index_comp_fr]
            #looking for index of the node may make the whole program very slow
            index_node = -1
            for k,othervalue in enumerate(cluster_nodes):
                if competency == othervalue[0]:
                    index_node = k
            if index_node >-1:
                added_score= frequency_value*((len(cluster_nodes[index_node][1].children)-1)**(3/2))
                score += added_score
                total += added_score
                
        #Afficher le graph       
        if Affichage_Comp:
            for pre,_,node in RenderTree(root):
                print("%s%s" % (pre,node.name))
        
    if total == 0 :
        raise Exception("Empty List")
    if Affichage_Comp:
        print("Compétences en commun, et score associé:")
        for k,value in enumerate(comp_communes):
            print(value, frequ_communes[k])
        print("Sous-Competences en commun:")
        for value in sous_comp_communes:
            print(value)
    return (score/total,score,total,competency_match,subcomptency_match)

def temp_function(my_mist, show):
    L=[]
    M=[]
    maximum_de_fréquence=[]
    for k, value in enumerate(my_mist):
        if value not in my_mist[:k]:
            L.append(0)
            M.append(value)
    for value in my_mist:
        i=M.index(value)
        L[i]+=1
        s = sum(L)
        #La liste des fréquences
        f=np.zeros(len(L))
    for k,value in enumerate(L):
        f[k]=-np.log(value/s)
    fprime = list(f)
    copie_fprime=fprime.copy()
    if show:
        nombre = input("Combien des fréquences les plus élevées voulez-vous voir ?"+"\r\n")
        i=0
        while i<int(nombre):
            #En esperant qu'il y aie jamais 2 fois la meme fréquence
            maximum_de_fréquence.append(max(fprime))
            fprime.remove(max(fprime))
            i+=1
        
        plt.plot(list(range(1,len(maximum_de_fréquence)+1)), maximum_de_fréquence,'o', color='black')
        plt.grid(True)
        plt.show()
        print('Compétences correspondantes:' +'\r\n')
        for k,value in enumerate(maximum_de_fréquence):
            index_competency= copie_fprime.index(value)
            copie_fprime[index_competency]=-1
            print(k+1,':',M[index_competency])
    return M, copie_fprime


def frequence(ontology, show=True, return_frequency_list=False):
    '''
    Desc. Calcule la liste des fréquences des compétences. Attention renvoie -log(1/f) à chaque fois
    '''
    competences = ontology.competences
    sous_competences = ontology.sous_competences
    if return_frequency_list:
        return temp_function(competences, show)
    else:
        temp_function(sous_competences, show)
        return ('Valeurs',maximum_de_fréquence) 

         


def PlusProcheMetierVoisinListe(L :list, Job :str,M:list,frequency_list:list):
    '''
    Desc. Fonction intermédiare; appelée par MetierLePlusProche
    '''
    H=[]
    while len(H)<5:
        index_closest_job=0
        distance_maximum = distance(L,Job,L[index_closest_job][0],M,frequency_list)[0]
        for index,value in enumerate(L):
            job_example=value[0]
            if job_example != Job and job_example not in [H[k][0] for k in range(len(H))]:
                dist = distance(L,Job,job_example,M,frequency_list)[0]
                if dist > distance_maximum:
                    index_closest_job =  index
                    distance_maximum = dist
        H.append((L[index_closest_job][0], distance_maximum))
    return [H[0],H]

def MetierLePlusProche(Job, show_competences = True):
    ontology = Internal_Ontology()
    L= ontology.L
    G,frequency_list=frequence(ontology, show=True, return_frequency_list=True)
    Closest_job,M =PlusProcheMetierVoisinListe(L,Job,G,frequency_list)
    t_1=time.time()
    if show_competences: 
        for k,value in enumerate(M):
            Job_to_compare_with=value[0]
            useless_variable1,useless_variable2,useless_variable3,competency_match,subcompetency_match=distance(L,Job,Job_to_compare_with,G,frequency_list)
            M[k]+=(('competency_match: ',competency_match),('subcompetency_match:',subcompetency_match))
        #print(time.time()-t_1)
        return Closest_job,M,time.time()-t_1
    else:
        #print(time.time()-t_1)
        return Closest_job,M,time.time()-t_1
    
def print_jobs():
    ''' available jobs'''
    L= Internal_Ontology().L    
    List_of_jobs = [L[k][0] for k in range(1,len(L))]
    for value in List_of_jobs:
        print(value)
    print("\r\n Ci-dessus la Liste des métiers disponibles")


print(MetierLePlusProche('Toxicologue industriel'))
