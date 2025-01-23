import streamlit as st
from streamlit_option_menu import option_menu
from nltk.tokenize import sent_tokenize
import string
from streamlit_option_menu import option_menu

import random


import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# SETTING THE LAYOUT AND GIVE PAGE TITLE AND ICON FOR THE APP
st.set_page_config(page_title='CHATBOT', page_icon='pic124.jpg',layout="wide")

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


with st.sidebar:
   selected1 = option_menu("Home", ["Introduction",'Chat With Me','Contact Us'], 
    icons=['lightbulb', 'book','telephone'], 
    menu_icon="house-door", default_index=0, 
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "17px"}, 
        "nav-link": {"font-size": "17px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "black"},
    }
)




if selected1=='Introduction':
       selected = option_menu("CHATBOT", ['Old Age Assistance'], 
    icons=[''], 
    menu_icon="bezier", default_index=0, 
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#FF4B4B"},
    }
)

       original_title = '<p style="font-family:Arial; color:#37333F; font-size: 18px;"><b>This chatbot is a web application developed using streamlit package in python. The app focuses with old age people staying alone who have no one to interact. It provides various kinds of help regarding health care like symptom diagnosis, helps in stress management and also provide guidance to physical hygiene. This application helps them to give necessary information and make them feel they are not alone.</b></p>'
       st.markdown(original_title, unsafe_allow_html=True)
       st.image('pic123.jpeg')



if selected1=='Chat With Me':
    selected = option_menu("Chat With Me", ['An Intelligent Chatbot'], 
    icons=[''], 
    menu_icon="bezier", default_index=0, 
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#FF4B4B"},
    }
)
    name='Gokul'
    name=st.text_input('Enter Your Name:')
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
    user_response = st.text_area('Enter your Message:')
    list.append(user_response)
    if st.button('Send'):
           user_response = user_response.lower()
           if(user_response!='bye'):
             if(user_response=='thanks'or user_response=='thankyou'):
               flag=False
               list.append("CHATBOT: Your welcome")
             elif(user_response=='how are you' or user_response== 'how you doing'):
               flag=False
               list.append('CHATBOT: Im Fine.. Thanks.. What about you') 
             elif(user_response=='im fine'):
               flag=False
               list.append('CHATBOT: Thats awesome')   
             else:
               if(greeting(user_response)!=None):
                list.append("CHATBOT:"+greeting(user_response))
               else:
                a='chatbot: '+response(user_response)
                list.append(a)
                sent_tokens.remove(user_response)      
           else: 
            list.append("CHATBOT: Bye! take care..")
           for i in range(0,len(list),2):
               abc=name+": "+list[i]
               st.success(abc)
               st.error(list[i+1])


if selected1=='Contact Us':
    selected = option_menu(None, ['Contact Us'], 
    icons=[''], 
    menu_icon="bezier", default_index=0, 
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#FF4B4B"},
    }
) 

    selected = option_menu(None, ['Gokul Riju - gokul@gmail.com','Abhinav S - abhinav@gmail.com','Maneesh Shibhu - maneesh@gmail.com','Devadarsh B - devu@gmail.com'], 
    icons=[''], 
    menu_icon="bezier", default_index=-1, 
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#FF4B4B"},
    }
) 
