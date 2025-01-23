import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components
import string
import nltk
import re
nltk.download('conll2000')
nltk.download('averaged_perceptron_tagger')
from nltk.corpus import conll2000
from nltk.chunk.util import tree2conlltags,conlltags2tree
from nltk.tag import UnigramTagger,BigramTagger
from nltk.chunk import ChunkParserI
from nltk.tree import *
import matplotlib.pyplot as plt

# Adjective keywords and conjunction keywords
select_keywords=["get","find","fetch"]
average_keywords=["average", "avg", "Average"]
sum_keywords=["sum", "total"]
max_keywords=["maximum", "highest", "max"]
min_keywords=["minimum", "lowest", "min"]
count_keywords=["number", "how many", "count"]
and_keywords=["and"]
or_keywords=["or"]
greater_keywords=["greater", "over","more"]
less_keywords=["lesser","under","less"]
equal_keywords=["is","equal","equals","equal to","equals to","are","can","will"]
not_keywords=["not","is'nt"]
between_keywords=["between","per","range"]
order_keywords=["order","ordered"]
asc_keywords=["ascending", "increasing"]
desc_keywords=["descending","decreasing","inverse","reverse","opposite"]
group_keywords=["group", "grouped","clubbed"]
negation_keywords=["not","no"]

like_keywords=["like","likes","similar to"]
distinct_keywords=["distinct","different","distinctive","distinctly","unique"]


# extract the POS Tags from the CONLL2000 dataset
def conll_tag_chunks(chunk_sents):
    tagged_sents = [tree2conlltags(tree) for tree in chunk_sents]
    return [[(t, c) for (w, t, c) in sent] for sent in tagged_sents]

# Apply sequential tagging to a sentence so that most suitable tagger is used to show POS Tag to corresponding word
def combined_tagger(train_data, taggers, backoff=None):
    for tagger in taggers:
        backoff = tagger(train_data, backoff=backoff)
    return backoff
#Class creating a chunk (collection of words) with the collective POS Tags
@st.cache
class NGramTagChunker(ChunkParserI):
    def __init__(self,train_sentences,tagger_classes=[UnigramTagger,BigramTagger]):
        train_sent_tags=conll_tag_chunks(train_sentences)
        self.chunk_tagger=combined_tagger(train_sent_tags,tagger_classes)
    def parse(self,tagged_sentence):
        if not tagged_sentence:
            return None
        pos_tags=[tag for word, tag in tagged_sentence]
        chunk_pos_tags=self.chunk_tagger.tag(pos_tags)
        chunk_tags=[chunk_tag for (pos_tag,chunk_tag) in chunk_pos_tags]
        wpc_tags=[(word,pos_tag,chunk_tag) for ((word,pos_tag),chunk_tag) in zip(tagged_sentence,chunk_tags)]
        return conlltags2tree(wpc_tags)

# Count and get the Common Nouns, i.e the attributes and table names
def Count_Nouns(chunk_tree):
    attr_or_table_count=0
    Noun_List=[]
    Possible_TableNoun_list=[]
    for t in chunk_tree:
        flag=0
        Noun=""
        Possible_TableNoun=""
        if type(t) is not tuple:
            for t2_i in range(0,len(t)):

                if (t[t2_i][1]=="NN" or t[t2_i][1]=="NNS" or t[t2_i][1]=="JJ") and ("'" in t[t2_i][0]):
                    st.write(t[t2_i][0])
                    Possible_TableNoun+=t[t2_i][0]
                    continue
                if t2_i==0:
                    if t[t2_i][1] == "NN" or t[t2_i][1] == "NNS":
                        Noun +=t[t2_i][0]
                        attr_or_table_count += 1
                        flag+=1
                elif t[t2_i][1]=="NN" or t[t2_i][1]=="NNS":
                    if (t[t2_i-1][1]=="NN" or t[t2_i-1][1]=="NNS"):
                        if Possible_TableNoun == t[t2_i-1][0]:
                            ind=Possible_TableNoun.index("'")
                            p=Possible_TableNoun[:ind]
                            ind=0
                            Noun=p+"."+t[t2_i][0]
                        else:
                            Noun+=" "+t[t2_i][0]
                    else:
                        Noun+=t[t2_i][0]
                    if flag==0:
                        attr_or_table_count += 1
                        flag+=1
            if len(Noun)!=0:

                Noun_List.append(Noun)
            if len(Possible_TableNoun)!=0:
                #st.write(Possible_TableNoun)
                #st.write(Possible_TableNoun)
                Possible_TableNoun_list.append(Possible_TableNoun)

        #st.write(Noun)
    #st.write(Possible_TableNoun_list)
    return Noun_List,attr_or_table_count,Possible_TableNoun_list

# Count and get the Proper Nouns, i.e the attributes values
def Count_Proper_Noun(chunk_tree):
    attr_or_table_count = 0
    Noun_List = []
    Noun = ""
    for t in chunk_tree:
        flag = 0
        Noun = ""
        if type(t) is not tuple:
            for t2_i in range(0, len(t)):
                if t2_i == 0:
                    if t[t2_i][1] == "NNP" or t[t2_i][1] == "CD" or t[t2_i][1]=="NNPS":
                        if t[t2_i][1] != "CD":
                            Noun += t[t2_i][0]
                            attr_or_table_count += 1
                            flag += 1
                        else:
                            #Noun=int(t[t2_i][0])
                            Noun = t[t2_i][0]
                            attr_or_table_count += 1
                            flag += 1
                elif t[t2_i][1] == "NNP" or t[t2_i][1] == "CD" or t[t2_i][1]=="NNPS":
                    if t[t2_i - 1][1] == "NNP" or t[t2_i - 1][1] == "CD" or t[t2_i][1]=="NNPS":
                        if t[t2_i][1] != "CD":
                            Noun += " " + t[t2_i][0]
                        else:
                            #Noun = int(t[t2_i][0])
                            Noun = t[t2_i][0]
                    else:
                        Noun += t[t2_i][0]
                    if flag == 0:
                        attr_or_table_count += 1
                        flag += 1
            if Noun !="":
                Noun_List.append(Noun)
        #st.write(Noun)
    #st.write(attr_or_table_count)
    return Noun_List, attr_or_table_count
# Create the attribute list in where clause
def Table_Attr_Where_Noun_Separater(chunk_tree,Noun_list,Proper_Noun_list):
    last_ind = len(Noun_list)-len(Proper_Noun_list)
    #st.write(Noun_list[0:last_ind])
    Table_Attr_Nouns = Noun_list[0:last_ind]
    Where_Nouns=Noun_list[last_ind:]

    # for i in range(len(Proper_Noun_list)):
    #     st.write(Noun_list[len(Noun_list)-len(Proper_Noun_list)-i])
    #     st.write(Proper_Noun_list[i])
    # st.write(Table_Attr_Nouns)

    return Table_Attr_Nouns,Where_Nouns

# create the query using SELECT clause, FROM clause and WHERE clause

def Agg(chunk_tree,Attr_Nouns):
    ANind=0
    for t in chunk_tree:
        if ANind==len(Attr_Nouns):
            break
        if type(t) is not tuple:
            for t2 in t:
                if t2[0] in Attr_Nouns:
                    pass
def Where_Condition_Check(chunk_tree,Table_Attr_Nouns,Where_Nouns,Proper_Noun_list):
    wherestr="WHERE "
    #st.write(Table_Attr_Nouns)
    #st.write(Where_Nouns)
    #st.write(Proper_Noun_list)
    T_A_Noun_ind=0#Traversing through the nouns that are tables and attributes
    Where_Nouns_ind=0#Traversing through nouns selected for where clause
    relation="AND"
    openFlag=0
    symbol="="
    for t in chunk_tree:
        if T_A_Noun_ind == len(Table_Attr_Nouns):
            proper_noun_multi_check=0
            for t2 in t:

                if openFlag==1:

                    if t2[0] in equal_keywords:

                        if symbol != "!=":
                            symbol="="
                        else:
                            symbol="!="
                        #st.write("Found equal to keyword", t2[0])
                        if proper_noun_multi_check == 1:
                            proper_noun_multi_check = 0
                    elif t2[0] in greater_keywords:
                        if symbol=="!=":
                            #st.write(t2[0])
                            symbol="<"
                        else:
                            #st.write(t2[0])
                            symbol=">"
                        #st.write("Found greater keyword",t2[0])
                        if proper_noun_multi_check == 1:
                            proper_noun_multi_check = 0
                    elif t2[0] in less_keywords:
                        if symbol=="!=":
                            #st.write(t2[0])
                            symbol=">"
                        else:
                            #st.write(t2[0])
                            symbol = "<"
                        #st.write("Found lesser keyword",t2[0])
                        if proper_noun_multi_check == 1:
                            proper_noun_multi_check = 0
                    elif t2[0] in not_keywords:
                        symbol="!="
                        # st.write("Found not keyword",t2[0])
                        if proper_noun_multi_check == 1:
                            proper_noun_multi_check = 0
                    else:
                        for ele in Proper_Noun_list:
                            #check for space between two words and checking those individual words are matching the current word
                            ele=ele.split(" ")
                            if t2[0] in ele:
                                #st.write(t2[0])
                                if proper_noun_multi_check==0:
                                    wherestr += Where_Nouns[Where_Nouns_ind] + symbol + Proper_Noun_list[Where_Nouns_ind]
                                    proper_noun_multi_check=1
                                elif proper_noun_multi_check==1:
                                    continue
                                symbol = "="
                                Where_Nouns_ind+=1
                        if t2[0] in and_keywords:
                            wherestr+=" AND "
                            openFlag = 0
                            if proper_noun_multi_check == 1:
                                proper_noun_multi_check=0
                        elif t2[0] in or_keywords:
                            wherestr+=" OR "
                            openFlag = 0
                            if proper_noun_multi_check == 1:
                                proper_noun_multi_check=0
                        elif t2[0] in negation_keywords:
                            wherestr+=" NOT "
                            openFlag = 0
                            if proper_noun_multi_check == 1:
                                proper_noun_multi_check=0
                elif openFlag==0:
                    #st.write(t2[0], t2[1])
                    if t2[0] in Where_Nouns:
                        relation="AND"
                        openFlag = 1
                        if proper_noun_multi_check == 1:
                            proper_noun_multi_check = 0




        else:
            if "." in Table_Attr_Nouns[T_A_Noun_ind]:
                Nouns = Table_Attr_Nouns[T_A_Noun_ind].split(".")
                Table_Attr_Nouns[T_A_Noun_ind] = Nouns[1]
            for t2 in t:
                if t2[0]==Table_Attr_Nouns[T_A_Noun_ind]:
                    T_A_Noun_ind+=1
    if wherestr!="WHERE ":
        #wherestr=wherestr[:len(wherestr)-5]
        wherestr+=";"
        #
        return  wherestr,1
    else:
        return wherestr,0

def SelectClause(chunk_tree,Table_Attr_Nouns,Where_Nouns,Proper_Noun_list,Possible_Table_Noun_list):
    Table_Noun=[]
    Attr_Noun=[]
    flag=0
    Table_Flag=0
    if len(Possible_Table_Noun_list)!=0:
        Table_Flag=1
        for t in Possible_Table_Noun_list:
            if "'" in t:
                ind=t.index("'")
                t=t[:ind]
            if t not in Table_Noun:
                Table_Noun.append(t)
    #st.write(Table_Attr_Nouns)
    if len(Table_Attr_Nouns)==1:
        Table_Noun.append(Table_Attr_Nouns[0])
        Attr_Noun.append("*")
    else:
        #Table_Noun.append(Table_Attr_Nouns[len(Table_Attr_Nouns)-1])
        #for i in range(len(Table_Attr_Nouns)-1):
        #    Attr_Noun.append(Table_Attr_Nouns[i])
        if Table_Flag==0:
            flag2=0
            TAind=0

            for t in chunk_tree:
                if TAind==len(Table_Attr_Nouns):
                    break
                if type(t) is not tuple:
                    for t2 in t:
                        if t2[0] == Table_Attr_Nouns[TAind]:
                            if flag2==1:
                                Table_Noun.append(Table_Attr_Nouns[TAind])
                                TAind+=1
                            else:
                                TAind+=1
                        if t2[1]=="IN":
                            flag2=1
                        else:
                            flag2=0
        #st.write(Table_Noun)
        if len(Table_Noun)!=0:
            for t in Table_Attr_Nouns:
                if t not in Table_Noun:
                    Attr_Noun.append(t)
    Attrind=0
    Agg_ind_list=[]
    for t in range(len(chunk_tree)):
        if Attrind==len(Attr_Noun):
            break
        if type(chunk_tree[t]) is not tuple:
            for t2_ind in range(len(chunk_tree[t])):

                #st.write(chunk_tree[t][t2_ind][0])
                if chunk_tree[t][t2_ind][0]==Attr_Noun[Attrind]:
                    if t2_ind!=0:
                        if chunk_tree[t][t2_ind-1][1]=="JJ" or chunk_tree[t][t2_ind-1][1]=="JJS":
                            if chunk_tree[t][t2_ind-1][0] in average_keywords:
                                pass
                                #st.write(chunk_tree[t][t2_ind-1][0])
                                #st.write(chunk_tree[t][t2_ind][0])
                                #st.write(Attrind)
                                Agg_ind_list.append([Attrind,"AVG("])
                                #st.write("Found Average Aggregation")
                            elif chunk_tree[t][t2_ind-1][0] in min_keywords:
                                pass
                                #st.write(chunk_tree[t][t2_ind - 1][0])
                                #st.write(chunk_tree[t][t2_ind][0])
                                #st.write(Attrind)
                                Agg_ind_list.append([Attrind,"MIN("])
                                #st.write("Found Minimum Aggregation")
                            elif chunk_tree[t][t2_ind-1][0] in max_keywords:
                                pass
                                #st.write(chunk_tree[t][t2_ind - 1][0])
                                #st.write(chunk_tree[t][t2_ind][0])
                                #st.write(Attrind)
                                Agg_ind_list.append([Attrind,"MAX("])
                                #st.write("Found Maximum Aggregation")
                            elif chunk_tree[t][t2_ind-1][0] in sum_keywords:
                                pass
                                #st.write(chunk_tree[t][t2_ind - 1][0])
                                #st.write(chunk_tree[t][t2_ind][0])
                                #st.write(Attrind)
                                Agg_ind_list.append([Attrind,"SUM("])
                                #st.write("Found Maximum Aggregation")
                    else:
                        if chunk_tree[t-1][len(chunk_tree[t-1])-1][0] in average_keywords:
                            pass
                            #st.write(chunk_tree[t-1][len(chunk_tree[t-1])-1][0])
                            #st.write(chunk_tree[t-1][len(chunk_tree[t-1])-1][0])
                            Agg_ind_list.append([Attrind, "AVG("])
                            #st.write("Found Average Aggregation")
                        elif chunk_tree[t-1][len(chunk_tree[t-1])-1][0] in min_keywords:
                            pass
                            #st.write(chunk_tree[t - 1][len(chunk_tree[t - 1]) - 1][0])
                            #st.write(chunk_tree[t - 1][len(chunk_tree[t - 1]) - 1][0])
                            Agg_ind_list.append([Attrind, "MIN("])
                            #st.write("Found Minimum Aggregation")
                        elif chunk_tree[t-1][len(chunk_tree[t-1])-1][0] in max_keywords:
                            pass
                            #st.write(chunk_tree[t - 1][len(chunk_tree[t - 1]) - 1][0])
                            #st.write(chunk_tree[t - 1][len(chunk_tree[t - 1]) - 1][0])
                            Agg_ind_list.append([Attrind, "MAX("])
                            #st.write("Found Maximum Aggregation")
                        elif chunk_tree[t-1][len(chunk_tree[t-1])-1][0] in sum_keywords:
                            pass
                            #st.write(chunk_tree[t - 1][len(chunk_tree[t - 1]) - 1][0])
                            #st.write(chunk_tree[t - 1][len(chunk_tree[t - 1]) - 1][0])
                            Agg_ind_list.append([Attrind, "SUM("])
                    Attrind+=1
    selectstr="SELECT "
    j=0

    #st.write(Agg_ind_list)
    #st.write(Attr_Noun)
    for i in range(len(Attr_Noun)):
        if j < len(Agg_ind_list):
            if i==Agg_ind_list[j][0]:
                #st.write(Agg_ind_list[j][0])
                selectstr+=Agg_ind_list[j][1]+Attr_Noun[i]+")"
                j+=1
            else:
                selectstr += Attr_Noun[i]
        else:
            selectstr+=Attr_Noun[i]
        if i<len(Attr_Noun)-1:
            selectstr+=","

    fromstr = "FROM "
    for i in range(len(Table_Noun)):
        fromstr+=Table_Noun[i]
        if i!=len(Table_Noun)-1:
            fromstr+=","


    st.write(selectstr)
    #st.write("WHERE ")
    wherestr,flag=Where_Condition_Check(chunk_tree, Table_Attr_Nouns, Where_Nouns, Proper_Noun_list)
    if flag==1:
        pass

        if orderbycheck == 1:
            if descFlag == 1:
                OrderByClause = "ORDER BY " + orderbyNoun + " DESC;"
                st.write(fromstr)
                st.write(wherestr[0:len(wherestr)-1])
                st.write(OrderByClause)
            elif descFlag == 0:
                OrderByClause = "ORDER BY " + orderbyNoun + ";"
                st.write(fromstr)
                st.write(wherestr[0:len(wherestr) - 1])
                st.write(OrderByClause)
        else:
            st.write(fromstr)
            st.write(wherestr)
    else:
        pass
        if orderbycheck == 1:
            if descFlag == 1:
                OrderByClause = "ORDER BY " + orderbyNoun + " DESC;"
                st.write(fromstr)
                st.write(OrderByClause)
            elif descFlag == 0:
                OrderByClause = "ORDER BY " + orderbyNoun + ";"
                st.write(fromstr)
                st.write(OrderByClause)
        else:
            st.write(fromstr,";")
    #st.write(wherestr)

#MAIN FUNCTION
st.title('Natural language to SQL query converter')

#(conll2000) Corpus of Chunked Noun data containing 10948 sentences

data=conll2000.chunked_sents()
train=data[:10700]
test=data[10700:]
#print(len(train),len(test))
#print(train[1])
wtc=tree2conlltags(train[1])
#print(wtc)
tree=conlltags2tree(wtc)
#print(tree)

ntc=NGramTagChunker(train)
#print(ntc.evaluate(test))

#sentence='No new emoji may be released in 2021 due to COVID-19 pandemic word'
#sentence='What is the average age of students whose name is Doe or age over 25?'
#sentence='Show the average age of students whose name is Doe or age over 25?'
#sentence='Find the average age of students whose name is Doe or age over 25?'
#sentence='who is the manufacturer of the order year 1998?'
#TypesOfQueries=['Select','Create','Insert','Delete']
#options=st.selectbox("Type of query",TypesOfQueries)
#st.write("You selected: ",options)


model=ntc.evaluate(test)
#st.markdown("**Chunk Accuracy**")
#st.write("Accuracy: ",model.accuracy())
#st.write("Precision: ",model.precision())
#st.write("Recall: ",model.recall())
#st.write("F-Measure: ",model.f_measure())
sentence=st.text_area("Enter the text below","What is the name and age of students whose name is Doe or age can be 25?")
if st.button("Click for SQL query"):

    if len(sentence)==0:
        st.markdown("**Enter the sentence**")
    else:
        # REMOVE SPECIAL CHARACTERS
        st.markdown("**The sentence is:**")
        st.write(sentence)
        for char in string.punctuation:
            if char=="'":
                continue
            elif char =='"':
                continue
            else:
                sentence=sentence.replace(char,'')
        if "data" in sentence:
            if " data " in sentence:
                sentence=sentence.replace(' data ','')
            elif("data " in sentence):
                sentence =sentence.replace('data ','')
            elif(" data" in sentence):
                sentence =sentence.replace(' data','')

        nltk_pos_tagged=nltk.pos_tag(sentence.split())


        ind_start=len(nltk_pos_tagged)-1
        ind_end=len(nltk_pos_tagged)-1
        #st.write(nltk_pos_tagged)
        orderbyNoun=""
        descFlag=0
        orderbycheck=0
        for i in range(len(nltk_pos_tagged)):

            if nltk_pos_tagged[i][0] in asc_keywords:
                orderbycheck=1
                ind_start=i
                if i != len(nltk_pos_tagged) - 1:
                    if nltk_pos_tagged[i+1][0] in order_keywords:
                        if i+1 != len(nltk_pos_tagged) - 1:
                            if nltk_pos_tagged[i+2][1] =="IN":
                                if i + 2 != len(nltk_pos_tagged) - 1:
                                    if nltk_pos_tagged[i+3][1] == "NN" or nltk_pos_tagged[i+3][1] == "NNS":
                                        descFlag=0
                                        orderbyNoun=nltk_pos_tagged[i+3][0]
                                        ind_end=i+3
            elif nltk_pos_tagged[i][0] in desc_keywords:
                orderbycheck=1
                ind_start = i
                if i != len(nltk_pos_tagged) - 1:
                    if nltk_pos_tagged[i + 1][0] in order_keywords:
                        if i + 1 != len(nltk_pos_tagged) - 1:
                            if nltk_pos_tagged[i + 2][1] == "IN":
                                if i + 2 != len(nltk_pos_tagged) - 1:
                                    if nltk_pos_tagged[i + 3][1] == "NN" or nltk_pos_tagged[i + 3][1] == "NNS":
                                        descFlag = 1
                                        orderbyNoun = nltk_pos_tagged[i + 3][0]
                                        ind_end = i + 3
        if orderbycheck==1:
            nltk_pos_tagged = nltk_pos_tagged[:ind_start] + nltk_pos_tagged[ind_end+1:]

        #st.write(nltk_pos_tagged)
        chunk_tree=ntc.parse(nltk_pos_tagged)
        Pos_Tags=[]
        if type(chunk_tree) is 'NoneType':
            st.markdown("**enter a sentence**")
        else:
            for t in range(len(chunk_tree)):
                new_tup = []
                new_tup_ind = 0
                if type(chunk_tree[t]) is tuple:
                    if chunk_tree[t][0]=="and" or chunk_tree[t][0]=="AND":
                        chunk_tree[t]=nltk.tree.Tree(0,[nltk.tree.Tree(0,["and","CC"])])
                    elif chunk_tree[t][0]=="or" or chunk_tree[t][0]=="OR":
                        chunk_tree[t] = nltk.tree.Tree(0, [nltk.tree.Tree(0, ["or", "CC"])])
                    elif chunk_tree[t][0]=="not" or chunk_tree[t][0]=="NOT":
                        chunk_tree[t] = nltk.tree.Tree(0, [nltk.tree.Tree(0, ["not", "CC"])])
                    else:
                        chunk_tree[t]=nltk.tree.Tree(0,[nltk.tree.Tree(0, [chunk_tree[t][0], chunk_tree[t][1]])])
                        #st.write(chunk_tree[t][0])
                        #st.write(chunk_tree[t][1])
                #st.write(type(chunk_tree[t]))
                #st.write(chunk_tree[t])
            sentence_list=sentence.split(' ')
            #st.write(sentence_list)
            sent_ind=0
            for t in range(len(chunk_tree)):
                for t2 in range(len(chunk_tree[t])):
                    if type(chunk_tree[t][t2]) is tuple:
                        chunk_tree[t][t2]=list(chunk_tree[t][t2])
                        chunk_tree[t][t2][0]=sentence_list[sent_ind]
                        sent_ind+=1
                    else:
                        chunk_tree[t][t2][0] = sentence_list[sent_ind]
                        sent_ind += 1
            for t in chunk_tree:
                strin=""
                pos_tags=[]

                for i in t:
                    strin+=i[0]+" "
                    pos_tags.append(i[1])
                #strin=strin[:len(strin)-1]
                #st.write(type(t))
                #st.write(strin)
                #st.write(pos_tags)
                Pos_Tags.append(pos_tags)
            st.markdown("**Below is the SQL query:**")
            Noun_list,attr_or_table_count,Possible_Table_Noun_list=Count_Nouns(chunk_tree)
            Proper_Noun_list,value_count=Count_Proper_Noun(chunk_tree)
            Table_Attr_Nouns,Where_Nouns=Table_Attr_Where_Noun_Separater(chunk_tree,Noun_list,Proper_Noun_list)

            SelectClause(chunk_tree,Table_Attr_Nouns,Where_Nouns,Proper_Noun_list,Possible_Table_Noun_list)



            #st.write('SELECT COUNT(employee)')
            #st.write("FROM company")
            #st.write('WHERE department="Human Resources"')
            #st.write('ORDER BY age DESC;')