# IMPORTING LIBRARIES
import streamlit as st
from streamlit_option_menu import option_menu
import requests
import pandas as pd
import numpy as np
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import time





@st.cache
def convert_df(data1):
     return data1.to_csv().encode('utf-8')










# DOWNLOAD AS CSV FILE
def filedownload(df):
    csv=df.to_csv(index=True)
    b64=base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="ppi_data.csv">Download csv file</a>' 
    return href










# SETTING THE LAYOUT AND GIVE PAGE TITLE AND ICON FOR THE APP
st.set_page_config(page_title='PPINA : Protein-Protein Interaction Analysis', page_icon='a.jpg',layout="wide")







# CREATING THE SIDEBAR
with st.sidebar:
    selected1 = option_menu("Home", ["Introduction", 'Tutorial','PPI Network Construction','Statistical Analysis','Contact Us'], 
        icons=['lightbulb', 'book','bezier','graph-up','telephone'], menu_icon="house-door", default_index=0)
    







# INTRODUCTION
if selected1=="Introduction":
    selected = option_menu("PPINA", ['PROTEIN-PROTEIN INTERACTION NETWORK ANALYZER'], 
        icons=[''], menu_icon="bezier", default_index=0)
    original_title = '<p style="font-family:Arial; color:white; font-size: 18px;"><b>PPINA is a web application tool which can be used for the construction of protein-protein interaction networks, its visualization and further analysis. The data for the protein-protein interaction network is collected from the String and BioGRID database. The tool also allows the user to create their own network by uploading the edge list. It provides a variety of features to analyze the networks for gaining biological and functional insights into the network.</b></p>'
    st.markdown(original_title, unsafe_allow_html=True)
    st.image('b.png')
    st.image('c.png',use_column_width=True)







# CONTACT US
if selected1=="Contact Us":
    selected3 = option_menu("Contact Us", ['Developers','Location'], 
        icons=['person','geo-alt'], menu_icon="telephone", default_index=0)
    if selected3=="Developers":
        st.write('Jisha R.C - jisha@gmail.com')
        st.write('Achu Pushpan - achup030801@gmail.com')
        st.write('Ashish Arvind Suryawanshi - ashisharvind333@gmail.com')
        st.write('Harinandanan N - hari@gmail.com')
        st.write('Midhun Manu - midhun@gmail.com')
    if selected3=="Location":
        st.write('Amrita Viswa Vidhyapeedtham,')
        st.write('Amritapuri Campus, Kollam,')
        st.write('Kerala, India')
        st.write('690456')





abc="abc"







# PPI NETWORK CONSTRUCTION
if selected1=='PPI Network Construction':
    selected2 = option_menu("PPI NETWORK CONSTRUCTION", ["Query a Single Protein", 'Query Multiple Proteins','Upload Interaction Data File'], 
        icons=['patch-question', 'patch-question','file-arrow-up'], menu_icon="bezier", default_index=0)
    if selected2=='Query a Single Protein':
        p1 = st.text_input('Protein Name : ', 'ACE2')
        p2 = st.text_input('Organism NCBI ID : ', '9606')
        if st.button('SEARCH'):
           try:
               
               url = 'https://string-db.org/api/tsv/network?identifiers=' + p1 + '&species='+p2
               
               r = requests.get(url)
               lines = r.text.split('\n') # pull the text from the response object and split based on new lines 
               data = [l.split('\t') for l in lines] # split each line into its components based on tabs
               
               df = pd.DataFrame(data[1:-1], columns = data[0]) 
               interactions = df[['preferredName_A', 'preferredName_B', 'score']] 
               global data1
               data1=pd.DataFrame()
               
               data1['Source']=interactions['preferredName_A']
               data1['Target']=interactions['preferredName_B']
               
               
               str='hello'
           except:
               st.image('d.png')
               str='ram'
 
           if str=='hello':
               a=p1+' Protein-Protein Interaction'
               st.title(a)
               col1,col2 = st.columns(2)
               with col2:  
                   st.image('E.png')
                   st.dataframe(data1)
                   csv = convert_df(data1)
               
                   st.download_button(
                   label="Download data as CSV",
                   data=csv,
                   file_name='ppi_data.csv',
                   mime='text/csv',
                   ) 
 



               with col1:
                   st.image('F.png')  
                   G = nx.from_pandas_edgelist(data1, 'Source', 'Target')
                   prot_net = Network(height='1000px', bgcolor='#222222', font_color='white')
                   prot_net.from_nx(G)
                   prot_net.repulsion(node_distance=420, central_gravity=0.33,
                       spring_length=110, spring_strength=0.10,
                       damping=0.95)
                   try:
                      path = '/tmp'
                      prot_net.save_graph(f'{path}/pyvis_graph.html')
                      HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

                   # Save and read graph as HTML file (locally
                   except:
                      path = 'html files'
                      prot_net.save_graph(f'{path}/pyvis_fil.html')
                      HtmlFile = open(f'{path}/pyvis_fil.html', 'r', encoding='utf-8')

                   # Load HTML file in HTML component for display on Streamlit page
                   components.html(HtmlFile.read(), height=600)
                   










             
             
                   

              
 
           
                  

   







    

