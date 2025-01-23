import streamlit as st

from nltk.tokenize import sent_tokenize
import string
from streamlit_option_menu import option_menu

import random


import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title='CHATBOT', page_icon='a.jpg')

import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('popular',quiet=True)
nltk.download('punkt')
nltk.download('wordnet')



def response(user_response):
   robo_response=''
   sent_tokens.append(user_response)
   TfidfVec=TfidfVectorizer(tokenizer=LemNormalize,stop_words='english')
   tfidf=TfidfVec.fit_transform(sent_tokens)
   vals=cosine_similarity(tfidf[-1],tfidf)
   idx=vals.argsort()[0][-2]
   flat=vals.flatten()
   flat.sort()
   req_tfidf=flat[-2]
   if(req_tfidf==0):
     robo_response=robo_response+"I am sorry! I dont undersand you"
     return robo_response
   else:
    robo_response=robo_response+ sent_tokens[idx]
    return robo_response



def greeting(sentence):
  for word in sentence.split():
    if word.lower() in GREETINGS_INPUTS:
      return random.choice(GREETINGS_RESPONSES)

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]


def LemNormalize(text):
   return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


selected = option_menu("CHAT WITH ME", ['INTELLIGENT CHATBOT FOR OLD AGE PEOPLE'], 
    icons=[''], 
    menu_icon="bezier", default_index=0, 
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "green"},
    }
)

f=open('CHATBOT.txt','r',errors='ignore') 
raw=f.read()
raw=raw.lower()


sent_tokens=nltk.sent_tokenize(raw)
word_tokens=nltk.word_tokenize(raw)
lemmer=nltk.stem.WordNetLemmatizer()
remove_punct_dict=dict((ord(punct),None) for punct in string.punctuation)

GREETINGS_INPUTS=("hello","hi","greetings","sup","what's up","hey",)
GREETINGS_RESPONSES=["hi","hey","nods","hi there","hello","I am glad! Y0u are talking to me"]


flag=True
list=[]
st.success("chatbot: . I will answer your queries about symptoms of disease and helps in stress managment & sanitation for elderly people . If you want to exit, type Bye!")
user_response = st.text_area('Enter your Message :')
list.append(user_response)
if st.button('Send'):
           #user_response = text
           user_response = user_response.lower()
           if(user_response!='bye'):
             if(user_response=='thanks'or user_response=='thankyou'):
               flag=False
               list.append("chatbot: Your welcome")
             else:
               if(greeting(user_response)!=None):
                list.append("chatbot:"+greeting(user_response))
               else:
                a='chatbot: '+response(user_response)
                list.append(a)
                sent_tokens.remove(user_response)      
           else: 
            list.append("chatbot: Bye! take care..")
           for i in range(0,len(list),2):
               st.success(list[i])
               st.error(list[i+1])









