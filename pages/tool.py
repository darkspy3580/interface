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
import matplotlib.pyplot as plt
from networkx.algorithms.community.centrality import girvan_newman

import Bio


import sys
from Bio import Entrez


def get_tax_id(species):
    """to get data from ncbi taxomomy, we need to have the taxid. we can
    get that by passing the species name to esearch, which will return
    the tax id"""
    species = species.replace(' ', "+").strip()
    search = Entrez.esearch(term = species, db = "taxonomy", retmode = "xml")
    record = Entrez.read(search)
    return record['IdList'][0]

def get_tax_data(taxid):
    """once we have the taxid, we can fetch the record"""
    search = Entrez.efetch(id = taxid, db = "taxonomy", retmode = "xml")
    return Entrez.read(search)







 









@st.cache_data
def convert_df(data1):
     return data1.to_csv().encode('utf-8')










# DOWNLOAD AS CSV FILE
def filedownload(df):
    csv=df.to_csv(index=True)
    b64=base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="ppi_data.csv">Download csv file</a>' 
    return href
























# BACKGROUND COLOR - 
#86AF2D


# SETTING THE LAYOUT AND GIVE PAGE TITLE AND ICON FOR THE APP
st.set_page_config(page_title='PPINA : Protein-Protein Interaction Network Analysis', page_icon='a.jpg',layout="wide")






# CREATING THE SIDEBAR
with st.sidebar:
   selected1 = option_menu("Home", ["Introduction", 'Tutorial','PPI Network Construction','NCBI Organism ID Finder','Contact Us'], 
    icons=['lightbulb', 'book','bezier','123','telephone'], 
    menu_icon="house-door", default_index=0, 
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "17px"}, 
        "nav-link": {"font-size": "17px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "black"},
    }
)




selected2='a'


# PPI NETWORK CONSTRUCTION
if selected1=="PPI Network Construction":
    with st.sidebar:
        selected2 = option_menu("PPI Network Construction", ["Query a Single Protein", 'Query Multiple Proteins','Upload Edge List of Protein Interactions'], 
    icons=['patch-question', 'patch-question','file-arrow-up'], 
    menu_icon="bezier", default_index=0, 
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "17px"}, 
        "nav-link": {"font-size": "17px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "black"},
    }
)
        










# CONTACT US
if selected1=="Contact Us":
    with st.sidebar:
        selected3 = option_menu("Contact Us", ["Developers", 'Location'], 
    icons=['person','geo-alt'], 
    menu_icon="telephone", default_index=0, 
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "17px"}, 
        "nav-link": {"font-size": "17px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "black"},
    }
)

    if selected3=='Developers':
              st.title('Developers')
              st.write('Jisha R C - jisha@gmail.com')   
              st.write('Achu Pushpan - achu@gmail.com')
              st.write('Ashish Arvind Suryawanshi- ashish@gmail.com')
              st.write('Harinandanan N - hari@gmail.com')
              st.write('Midhun Manu - midhun@gmail.com')  

    if selected3=='Location':
              st.title('Location')
              st.write('Amrita Viswa Vidyapeetham')
              st.write('Amrita School of Engineering')
              st.write('Amritapuri')
              st.write('Kollam')  







# INTRODUCTION
if selected1=="Introduction":
    selected = option_menu("PPINA", ['PROTEIN-PROTEIN INTERACTION NETWORK ANALYZER'], 
    icons=[''], 
    menu_icon="bezier", default_index=0, 
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "green"},
    }
)
    original_title = '<p style="font-family:Arial; color:#37333F; font-size: 18px;"><b>PPINA is a web application tool which can be used for the construction of protein-protein interaction networks, its visualization and further analysis. The data for the protein-protein interaction network is collected from the String database. The tool also allows the user to create their own network by uploading the edge list. It provides a variety of features to analyze the networks for gaining biological and functional insights into the network.</b></p>'
    st.markdown(original_title, unsafe_allow_html=True)
    selected = option_menu(None, ['Sample Visualization of PPI Network'], 
    icons=['bezier'], 
    menu_icon="", default_index=0, 
    styles={
        "container": {"padding": "0!important", "background-color": "black"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "20px","text-color":"black", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "black"},
    }
)

    st.image('ae.png')













selected4='b'



# QUERY A SINGLE PROTEIN
if selected2=='Query a Single Protein':
    selected = option_menu("PPI NETWORK CONSTRUCTION", ['Query a Single Protein'], 
    icons=['patch-question'], 
    menu_icon="bezier", default_index=0, 
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "green"},
    }
)
    p1 = st.text_input('Protein Name : ', 'ACE2')
    p2 = st.text_input('Organism NCBI ID : ', '9606')
    selected4 = option_menu(None, ["Get PPI Data", "Visualize Network", 
        "Statistical Analysis", 'Topological Analysis'], 
    icons=['file-bar-graph', 'bezier', "graph-up", 'graph-up'], 
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "black"},
    }
)




    # GET PPI DATA
    if selected4=="Get PPI Data":
           try:
               url = 'https://string-db.org/api/tsv/network?identifiers=' + p1 + '&species='+p2
               
               r = requests.get(url)
               
               lines = r.text.split('\n') # pull the text from the response object and split based on new lines 
               
               data = [l.split('\t') for l in lines] # split each line into its components based on tabs
               
               df = pd.DataFrame(data[1:-1], columns = data[0]) 
               interactions = df[['preferredName_A', 'preferredName_B', 'score']] 
               data1=pd.DataFrame()
              
               data1['Source']=interactions['preferredName_A']
               data1['Target']=interactions['preferredName_B']
               a=p1+' Protein-Protein Interaction'
               st.title(a)
               st.dataframe(data1)
               csv = convert_df(data1)
               
               st.download_button(
                   label="Download data as CSV",
                   data=csv,
                   file_name='ppi_data.csv',
                   mime='text/csv',
                   )
           except:
               st.write(p1)
               st.image('d.png')








    # VISUALIZE NETWORK
    if selected4=='Visualize Network':
        try:
               selected5 = option_menu(None, ["Customize Nodes", "Customize Edges", 
        "View Full Screen","Exit Full Screen"], 
    icons=['pencil', 'pencil', "fullscreen", 'fullscreen-exit'], 
    menu_icon="cast", default_index=3, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "green"},
    }
)
               url = 'https://string-db.org/api/tsv/network?identifiers=' +p1+'&species='+p2
               
               r = requests.get(url)
               lines = r.text.split('\n') # pull the text from the response object and split based on new lines 
               data = [l.split('\t') for l in lines] # split each line into its components based on tabs
               
               df = pd.DataFrame(data[1:-1], columns = data[0]) 
               interactions = df[['preferredName_A', 'preferredName_B', 'score']] 
               data1=pd.DataFrame()
               
               data1['Source']=interactions['preferredName_A']
               data1['Target']=interactions['preferredName_B']
               G = nx.from_pandas_edgelist(data1, 'Source', 'Target')
               a='50%'
               if selected5=="Exit Full Screen":
                    a='50%'
               if selected5=="View Full Screen":
                    a='100%'
               prot_net = Network(height='1000px',width=a, bgcolor='#222222', font_color='white')
               prot_net.from_nx(G)
               prot_net.repulsion(node_distance=420, central_gravity=0.33,
                       spring_length=110, spring_strength=0.10,
                       damping=0.95)
               if selected5=="Customize Nodes":
                    prot_net.show_buttons(filter_=['nodes'])
                    a='50%'
               if selected5=="Customize Edges":
                    prot_net.show_buttons(filter_=['edges'])
                    a='50%'
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



               c1 = nx.number_of_nodes(G)
               c2 = nx.number_of_edges(G)
               c1="Proteins : "+str(c1)
               c2="Interactions : "+str(c2)
               selected = option_menu(None, ["Network Overview"], 
    icons=['lightbulb'], 
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "black"},
    }
)
               selected = option_menu(None, [c1,c2], 
    icons=['circle','arrow-right'], 
    menu_icon="cast", default_index=-1, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#fafafa"},
    }
)
        except:
           st.image('d.png')
                         
        
  







    # STATISTICAL ANALYSIS
    if selected4=='Statistical Analysis':
        try:
               url = 'https://string-db.org/api/tsv/network?identifiers=' +p1+'&species='+p2
               
               r = requests.get(url)
               lines = r.text.split('\n') # pull the text from the response object and split based on new lines 
               data = [l.split('\t') for l in lines] # split each line into its components based on tabs
               
               df = pd.DataFrame(data[1:-1], columns = data[0]) 
               interactions = df[['preferredName_A', 'preferredName_B', 'score']] 
               data1=pd.DataFrame()
               
               data1['Source']=interactions['preferredName_A']
               data1['Target']=interactions['preferredName_B']
               G = nx.from_pandas_edgelist(data1, 'Source', 'Target')
               col1,col2=st.columns(2)



               with col1:
                   selected7 = option_menu("STATISTICAL PARAMETERS", ['Number of Nodes','Number of Edges','Average Degree','Average Path Length',"Network Diameter","Network Radius","Average Clustering Coefficient",'Clustering Coefficient of each node',"Connected or Disconnected","Number of Connected Components","Center","View Full Statistics"], 
    icons=['123','123','123','123','123','123','123','123','123','123','123','123'], 
    menu_icon="graph-up", default_index=0, 
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa",'border': '7px solid powderblue'},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "green"},
    }
)




               with col2:
                   if selected7=="Number of Nodes":
                         c1=nx.number_of_nodes(G)
                         str= 'Number of Nodes : '+str(c1)
                         st.header(str)
                   if selected7=="Number of Edges":
                         c2=nx.number_of_edges(G)
                         str= 'Number of Edges : '+str(c2)
                         st.header(str)
                   if selected7=="Average Degree":
                         try: 
                            G_deg=nx.degree_histogram(G)
                            G_deg_sum=[a*b for a,b in zip(G_deg,range(0,len(G_deg)))]
                            avg_deg=sum(G_deg_sum)/nx.number_of_nodes(G)
                            str='Average Degree : '+str(avg_deg)
                            st.header(str)



                         except:
                             st.header('Average Degree cannot be found')

                   if selected7=="Average Path Length":
                         try:
                             c3=nx.average_shortest_path_length(G)
                             str='Average Path Length : '+str(c3) 
                             st.header(str)
                         except:
                              st.header('Average Path Length cannot be found')

                   if selected7=="Network Diameter":
                           try:
                              c4=nx.diameter(G)
                              str='Network Diameter : '+str(c4) 
                              st.header(str)
                           except:
                              st.header('Network Diameter cannot be found')
                   if selected7=="Network Radius":
                           try:
                              c5=nx.radius(G)
                              str='Network Radius : '+str(c5) 
                              st.header(str)
                           except:
                              st.header('Network Radius cannot be found')
                   if selected7=="Average Clustering Coefficient":
                           try:
                              G_cluster = sorted(list(nx.clustering(G).values()))
                              avg_clu=sum(G_cluster)/len(G_cluster)
                              str='Average Clustering Coefficient : '+str(avg_clu) 
                              st.header(str)
                           except:
                              st.header('Average Clustering Coefficient cannot be found')
                   if selected7=="Clustering Coefficient of each node":
                           try:
                              c6=nx.clustering(G)
                              new = pd.DataFrame()
                              new['nodes']=c6.keys()
                              new['values']=c6.values()
                              str='Clustering Coefficient of each node : ' 
                              st.header(str)
                              st.dataframe(new)
                           except:
                              st.header('Clustering Coefficient of each node cannot be found')
                   if selected7=="Connected or Disconnected":
                           try:
                              c7=nx.is_connected(G)
                              if c7=='True':
                                  s='Connected'
                              else:
                                  s='Disconnected'
                              str='The Network is '+s 
                              st.header(str)
                           except:
                              st.header('Connectivity cannot be found')
                   if selected7=="Number of Connected Components":
                           try:
                              c7=nx.number_connected_components(G)
                              str='Number of Connected Components : '+str(c7) 
                              st.header(str)
                           except:
                              st.header('Number of Connected Components cannot be found. Since, the graph is disconnected')
                   if selected7=="Center":
                           try:
                              c8=nx.center(G)
                              str='Center : '+str(c8) 
                              st.header(str)
                           except:
                              st.header('Center cannot be found')

                   if selected7=="View Full Statistics":
                           try:
                              list1=['Number of Nodes','Number of Edges','Average Degree','Average Path Length',"Network Diameter","Network Radius","Average Clustering Coefficient","Number of Connected Components"]
                              try:
                                c1=nx.number_of_nodes(G)
                              except:
                                c1='Not Determined'
                              try:
                                 c2=nx.number_of_edges(G)
                              except:
                                  c2='Not Determined'
                              try:
                                 G_deg=nx.degree_histogram(G)
                                 G_deg_sum=[a*b for a,b in zip(G_deg,range(0,len(G_deg)))]
                                 avg_deg=sum(G_deg_sum)/nx.number_of_nodes(G)
                              except:
                                 avg_deg='Not Determined'
                              try:
                                 c3=nx.average_shortest_path_length(G)
                              except:
                                 c3='Not Determined'
                              try:
                                 c4=nx.diameter(G)
                              except:
                                 c4='Not Determined'
                              try:
                                 c5=nx.radius(G)
                              except:
                                 c5='Not Determined'
                              try:
                                  G_cluster = sorted(list(nx.clustering(G).values()))
                                  avg_clu=sum(G_cluster)/len(G_cluster)
                              except:
                                   avg_clu='Not Determined'
                              try:
                                 c7=nx.is_connected(G)
                              except:
                                  c7='Not Determined'
                              try:
                                  c8=nx.number_connected_components(G)
                              except:
                                   c8='Not Determined'
                              list2=[c1,c2,avg_deg,c3,c4,c5,avg_clu,c8]
                              data=pd.DataFrame()
                              data['Statistical Parameters'] = list1
                              data['Values'] = list2
                              st.header('STATISTICS')
                              st.dataframe(data)




                           except:
                              st.header('Wrong Input')
                   
               









        except:
            st.image('d.png')











    # TOPOLOGICAL ANALYSIS
    if selected4=='Topological Analysis':
        try:
               url = 'https://string-db.org/api/tsv/network?identifiers=' +p1+'&species='+p2
               
               r = requests.get(url)
               lines = r.text.split('\n') # pull the text from the response object and split based on new lines 
               data = [l.split('\t') for l in lines] # split each line into its components based on tabs
               
               df = pd.DataFrame(data[1:-1], columns = data[0]) 
               interactions = df[['preferredName_A', 'preferredName_B', 'score']] 
               data1=pd.DataFrame()
               
               data1['Source']=interactions['preferredName_A']
               data1['Target']=interactions['preferredName_B']
               G = nx.from_pandas_edgelist(data1, 'Source', 'Target')
               col1,col2=st.columns(2)


               with col1:
                   selected8 = option_menu("TOPOLOGICAL ANALYSIS", ['Centrality Analysis','Community Detections','Shortest Path'], 
    icons=['123','123','123'], 
    menu_icon="graph-up", default_index=0, 
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa",'border': '7px solid powderblue'},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "green"},
    }
)
              




               with col2:
                 if selected8=="Centrality Analysis":
                     option = st.selectbox(
     'Select the type of Centrality you want to Calculate',
     ('Degree Centrality', 'Closeness Centrality', 'Betweenness Centrality'))
                     if option=='Degree Centrality':
                         de1 = nx.degree_centrality(G)
                         selected9 = option_menu(None, ['Top 5 Proteins','View Centrality of all Proteins'], 
    icons=['123','123'], 
    menu_icon="graph-up", default_index=0, 
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "black"},
    }
)
                         if selected9== 'Top 5 Proteins':
                               # Sorting the Dictionary of de1
                               s_h = {k: v for k, v in sorted(de1.items(),                key=lambda item: item[1], reverse=True)}
                               i_aux = 0
                               new_SH = {}
                               for k,v in s_h.items():
                                   if i_aux < 5:
                                       new_SH[k] = v
                                       i_aux += 1
                                   else:
                                       break    
                               aux1=[]
                               for k in new_SH.keys():
                                    aux1.append(k)
                               index = [1,2,3,4,5]  
                               d2 = {'Degree' : aux1}
                               # Transferring d1,d2,d3,d4 into a single dictionary
                               data_Dic = dict(list(d2.items()))
                               dframe = pd.DataFrame(data_Dic,index=index)
                               st.write(dframe)
                         if selected9== 'View Centrality of all Proteins':
                               data=pd.DataFrame()
                               data['Proteins']=de1.keys()
                               data['Values']=de1.values()
                               st.dataframe(data)






                   
                     if option=='Closeness Centrality':
                         de1 = nx.closeness_centrality(G)
                         selected9 = option_menu(None, ['Top 5 Proteins','View Centrality of all Proteins'], 
    icons=['123','123'], 
    menu_icon="graph-up", default_index=0, 
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "black"},
    }
)
                         if selected9== 'Top 5 Proteins':
                               # Sorting the Dictionary of de1
                               s_h = {k: v for k, v in sorted(de1.items(),                key=lambda item: item[1], reverse=True)}
                               i_aux = 0
                               new_SH = {}
                               for k,v in s_h.items():
                                   if i_aux < 5:
                                       new_SH[k] = v
                                       i_aux += 1
                                   else:
                                       break    
                               aux1=[]
                               for k in new_SH.keys():
                                    aux1.append(k)
                               index = [1,2,3,4,5]  
                               d2 = {'Degree' : aux1}
                               # Transferring d1,d2,d3,d4 into a single dictionary
                               data_Dic = dict(list(d2.items()))
                               dframe = pd.DataFrame(data_Dic,index=index)
                               st.write(dframe)
                         if selected9== 'View Centrality of all Proteins':
                               data=pd.DataFrame()
                               data['Proteins']=de1.keys()
                               data['Values']=de1.values()
                               st.dataframe(data)









                     if option=='Betweenness Centrality':
                         de1 = nx.betweenness_centrality(G)
                         selected9 = option_menu(None, ['Top 5 Proteins','View Centrality of all Proteins'], 
    icons=['123','123'], 
    menu_icon="graph-up", default_index=0, 
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "black"},
    }
)
                         if selected9== 'Top 5 Proteins':
                               # Sorting the Dictionary of de1
                               s_h = {k: v for k, v in sorted(de1.items(),                key=lambda item: item[1], reverse=True)}
                               i_aux = 0
                               new_SH = {}
                               for k,v in s_h.items():
                                   if i_aux < 5:
                                       new_SH[k] = v
                                       i_aux += 1
                                   else:
                                       break    
                               aux1=[]
                               for k in new_SH.keys():
                                    aux1.append(k)
                               index = [1,2,3,4,5]  
                               d2 = {'Degree' : aux1}
                               # Transferring d1,d2,d3,d4 into a single dictionary
                               data_Dic = dict(list(d2.items()))
                               dframe = pd.DataFrame(data_Dic,index=index)
                               st.write(dframe)
                         if selected9== 'View Centrality of all Proteins':
                               data=pd.DataFrame()
                               data['Proteins']=de1.keys()
                               data['Values']=de1.values()
                               st.dataframe(data)

                 if selected8=="Community Detections":
                          communities = girvan_newman(G)
                          node_groups = []
                          i=1
                          for com in next(communities):
                               node_groups.append(list(com))

                          l=len(node_groups)
                          st.header('Communities : ')
                          for i in range(l):
                             da=pd.DataFrame()
                             da['community '+str(i)]=node_groups[i]
                             st.dataframe(da)



                 if selected8=="Shortest Path":
                         la=G.nodes()
                         lb=G.nodes()
                         st.header('Shortest Path Between two Proteins : ')
                         option1 = st.selectbox(
     'Source Protein ',
     la)
                         option2 = st.selectbox(
     'Target Protein ',
     lb)
                         if st.button('Find'):
                            try:        
                               l=nx.shortest_path(G,option1,option2)
                               str=''
                               for i in range(len(l)-1):
                                   str=str+l[i]+'--->'
                               str=str+l[len(l)-1]
                               abc="Shortest Path  Between "+option1+" and "+option2
                               selected = option_menu(abc, [str], 
    icons=[None], 
    menu_icon="signpost", default_index=0, 
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "black"},
    }
)
                             
                            except:
                               st.subheader('No Path Between '+option1+' and '+option2 )
                        
                         
                     











        except:
            st.image('d.png')
               





                   













            
# QUERY A MULTIPLE PROTEIN
if selected2=='Query Multiple Proteins':
    selected = option_menu("PPI NETWORK CONSTRUCTION", ['Query Multiple Proteins'], 
    icons=['patch-question'], 
    menu_icon="bezier", default_index=0, 
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "green"},
    }
)

    protein1 = st.text_area('List of Names : ', 'ACE2,MEP1A,DPP4,REN,MME,PRCP,SLC6A19,AGT,SLC1A7,CLEC4M,TMPRSS2')
    st.write('Note: The Proteins should be seperated by a comma. No spaces are allowed between the Proteins.')
    protein=protein1.split(',')
    p1 = '%0d'.join(protein)
    p2 = st.text_input('Organism NCBI ID : ', '9606')
    selected4 = option_menu(None, ["Get PPI Data", "Visualize Network", 
        "Statistical Analysis", 'Topological Analysis'], 
    icons=['file-bar-graph', 'bezier', "graph-up", 'graph-up'], 
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "black"},
    }
)




     # GET PPI DATA
    if selected4=="Get PPI Data":
           try:
               url = 'https://string-db.org/api/tsv/network?identifiers=' + p1 + '&species='+p2
               
               r = requests.get(url)
               
               lines = r.text.split('\n') # pull the text from the response object and split based on new lines 
               
               data = [l.split('\t') for l in lines] # split each line into its components based on tabs
               
               df = pd.DataFrame(data[1:-1], columns = data[0]) 
               interactions = df[['preferredName_A', 'preferredName_B', 'score']] 
               data1=pd.DataFrame()
              
               data1['Source']=interactions['preferredName_A']
               data1['Target']=interactions['preferredName_B']
               st.title('Protein-Protein Interaction Data')
               st.dataframe(data1)
               csv = convert_df(data1)
               
               st.download_button(
                   label="Download data as CSV",
                   data=csv,
                   file_name='ppi_data.csv',
                   mime='text/csv',
                   )
           except:
               st.write(p1)
               st.image('d.png')









    # VISUALIZE NETWORK
    if selected4=='Visualize Network':
        try:
               selected5 = option_menu(None, ["Customize Nodes", "Customize Edges", 
        "View Full Screen","Exit Full Screen"], 
    icons=['pencil', 'pencil', "fullscreen", 'fullscreen-exit'], 
    menu_icon="cast", default_index=3, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "green"},
    }
)
               url = 'https://string-db.org/api/tsv/network?identifiers=' +p1+'&species='+p2
               
               r = requests.get(url)
               lines = r.text.split('\n') # pull the text from the response object and split based on new lines 
               data = [l.split('\t') for l in lines] # split each line into its components based on tabs
               
               df = pd.DataFrame(data[1:-1], columns = data[0]) 
               interactions = df[['preferredName_A', 'preferredName_B', 'score']] 
               data1=pd.DataFrame()
               
               data1['Source']=interactions['preferredName_A']
               data1['Target']=interactions['preferredName_B']
               G = nx.from_pandas_edgelist(data1, 'Source', 'Target')
               a='50%'
               if selected5=="Exit Full Screen":
                    a='50%'
               if selected5=="View Full Screen":
                    a='100%'
               prot_net = Network(height='1000px',width=a, bgcolor='#222222', font_color='white')
               prot_net.from_nx(G)
               prot_net.repulsion(node_distance=420, central_gravity=0.33,
                       spring_length=110, spring_strength=0.10,
                       damping=0.95)
               if selected5=="Customize Nodes":
                    prot_net.show_buttons(filter_=['nodes'])
                    a='50%'
               if selected5=="Customize Edges":
                    prot_net.show_buttons(filter_=['edges'])
                    a='50%'
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



               c1 = nx.number_of_nodes(G)
               c2 = nx.number_of_edges(G)
               c1="Proteins : "+str(c1)
               c2="Interactions : "+str(c2)
               selected = option_menu(None, ["Network Overview"], 
    icons=['lightbulb'], 
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "black"},
    }
)
               selected = option_menu(None, [c1,c2], 
    icons=['circle','arrow-right'], 
    menu_icon="cast", default_index=-1, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#fafafa"},
    }
)
        except:
           st.image('d.png')
                         
        
  







    # STATISTICAL ANALYSIS
    if selected4=='Statistical Analysis':
        try:
               url = 'https://string-db.org/api/tsv/network?identifiers=' +p1+'&species='+p2
               
               r = requests.get(url)
               lines = r.text.split('\n') # pull the text from the response object and split based on new lines 
               data = [l.split('\t') for l in lines] # split each line into its components based on tabs
               
               df = pd.DataFrame(data[1:-1], columns = data[0]) 
               interactions = df[['preferredName_A', 'preferredName_B', 'score']] 
               data1=pd.DataFrame()
               
               data1['Source']=interactions['preferredName_A']
               data1['Target']=interactions['preferredName_B']
               G = nx.from_pandas_edgelist(data1, 'Source', 'Target')
               col1,col2=st.columns(2)



               with col1:
                   selected7 = option_menu("STATISTICAL PARAMETERS", ['Number of Nodes','Number of Edges','Average Degree','Average Path Length',"Network Diameter","Network Radius","Average Clustering Coefficient",'Clustering Coefficient of each node',"Connected or Disconnected","Number of Connected Components","Center","View Full Statistics"], 
    icons=['123','123','123','123','123','123','123','123','123','123','123','123'], 
    menu_icon="graph-up", default_index=0, 
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa",'border': '7px solid powderblue'},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "green"},
    }
)




               with col2:
                   if selected7=="Number of Nodes":
                         c1=nx.number_of_nodes(G)
                         str= 'Number of Nodes : '+str(c1)
                         st.header(str)
                   if selected7=="Number of Edges":
                         c2=nx.number_of_edges(G)
                         str= 'Number of Edges : '+str(c2)
                         st.header(str)
                   if selected7=="Average Degree":
                         try: 
                            G_deg=nx.degree_histogram(G)
                            G_deg_sum=[a*b for a,b in zip(G_deg,range(0,len(G_deg)))]
                            avg_deg=sum(G_deg_sum)/nx.number_of_nodes(G)
                            str='Average Degree : '+str(avg_deg)
                            st.header(str)



                         except:
                             st.header('Average Degree cannot be found')

                   if selected7=="Average Path Length":
                         try:
                             c3=nx.average_shortest_path_length(G)
                             str='Average Path Length : '+str(c3) 
                             st.header(str)
                         except:
                              st.header('Average Path Length cannot be found')

                   if selected7=="Network Diameter":
                           try:
                              c4=nx.diameter(G)
                              str='Network Diameter : '+str(c4) 
                              st.header(str)
                           except:
                              st.header('Network Diameter cannot be found')
                   if selected7=="Network Radius":
                           try:
                              c5=nx.radius(G)
                              str='Network Radius : '+str(c5) 
                              st.header(str)
                           except:
                              st.header('Network Radius cannot be found')
                   if selected7=="Average Clustering Coefficient":
                           try:
                              G_cluster = sorted(list(nx.clustering(G).values()))
                              avg_clu=sum(G_cluster)/len(G_cluster)
                              str='Average Clustering Coefficient : '+str(avg_clu) 
                              st.header(str)
                           except:
                              st.header('Average Clustering Coefficient cannot be found')
                   if selected7=="Clustering Coefficient of each node":
                           try:
                              c6=nx.clustering(G)
                              new = pd.DataFrame()
                              new['nodes']=c6.keys()
                              new['values']=c6.values()
                              str='Clustering Coefficient of each node : ' 
                              st.header(str)
                              st.dataframe(new)
                           except:
                              st.header('Clustering Coefficient of each node cannot be found')
                   if selected7=="Connected or Disconnected":
                           try:
                              c7=nx.is_connected(G)
                              if c7=='True':
                                  s='Connected'
                              else:
                                  s='Disconnected'
                              str='The Network is '+s 
                              st.header(str)
                           except:
                              st.header('Connectivity cannot be found')
                   if selected7=="Number of Connected Components":
                           try:
                              c7=nx.number_connected_components(G)
                              str='Number of Connected Components : '+str(c7) 
                              st.header(str)
                           except:
                              st.header('Number of Connected Components cannot be found. Since, the graph is disconnected')
                   if selected7=="Center":
                           try:
                              c8=nx.center(G)
                              str='Center : '+str(c8) 
                              st.header(str)
                           except:
                              st.header('Center cannot be found')

                   if selected7=="View Full Statistics":
                           try:
                              list1=['Number of Nodes','Number of Edges','Average Degree','Average Path Length',"Network Diameter","Network Radius","Average Clustering Coefficient","Number of Connected Components"]
                              try:
                                c1=nx.number_of_nodes(G)
                              except:
                                c1='Not Determined'
                              try:
                                 c2=nx.number_of_edges(G)
                              except:
                                  c2='Not Determined'
                              try:
                                 G_deg=nx.degree_histogram(G)
                                 G_deg_sum=[a*b for a,b in zip(G_deg,range(0,len(G_deg)))]
                                 avg_deg=sum(G_deg_sum)/nx.number_of_nodes(G)
                              except:
                                 avg_deg='Not Determined'
                              try:
                                 c3=nx.average_shortest_path_length(G)
                              except:
                                 c3='Not Determined'
                              try:
                                 c4=nx.diameter(G)
                              except:
                                 c4='Not Determined'
                              try:
                                 c5=nx.radius(G)
                              except:
                                 c5='Not Determined'
                              try:
                                  G_cluster = sorted(list(nx.clustering(G).values()))
                                  avg_clu=sum(G_cluster)/len(G_cluster)
                              except:
                                   avg_clu='Not Determined'
                              try:
                                 c7=nx.is_connected(G)
                              except:
                                  c7='Not Determined'
                              try:
                                  c8=nx.number_connected_components(G)
                              except:
                                   c8='Not Determined'
                              list2=[c1,c2,avg_deg,c3,c4,c5,avg_clu,c8]
                              data=pd.DataFrame()
                              data['Statistical Parameters'] = list1
                              data['Values'] = list2
                              st.header('STATISTICS')
                              st.dataframe(data)




                           except:
                              st.header('Wrong Input')
                   
               









        except:
            st.image('d.png')











    # TOPOLOGICAL ANALYSIS
    if selected4=='Topological Analysis':
        try:
               url = 'https://string-db.org/api/tsv/network?identifiers=' +p1+'&species='+p2
               
               r = requests.get(url)
               lines = r.text.split('\n') # pull the text from the response object and split based on new lines 
               data = [l.split('\t') for l in lines] # split each line into its components based on tabs
               
               df = pd.DataFrame(data[1:-1], columns = data[0]) 
               interactions = df[['preferredName_A', 'preferredName_B', 'score']] 
               data1=pd.DataFrame()
               
               data1['Source']=interactions['preferredName_A']
               data1['Target']=interactions['preferredName_B']
               G = nx.from_pandas_edgelist(data1, 'Source', 'Target')
               col1,col2=st.columns(2)


               with col1:
                   selected8 = option_menu("TOPOLOGICAL ANALYSIS", ['Centrality Analysis','Community Detections','Shortest Path'], 
    icons=['123','123','123'], 
    menu_icon="graph-up", default_index=0, 
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa",'border': '7px solid powderblue'},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "green"},
    }
)
              




               with col2:
                 if selected8=="Centrality Analysis":
                     option = st.selectbox(
     'Select the type of Centrality you want to Calculate',
     ('Degree Centrality', 'Closeness Centrality', 'Betweenness Centrality'))
                     if option=='Degree Centrality':
                         de1 = nx.degree_centrality(G)
                         selected9 = option_menu(None, ['Top 5 Proteins','View Centrality of all Proteins'], 
    icons=['123','123'], 
    menu_icon="graph-up", default_index=0, 
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "black"},
    }
)
                         if selected9== 'Top 5 Proteins':
                               # Sorting the Dictionary of de1
                               s_h = {k: v for k, v in sorted(de1.items(),                key=lambda item: item[1], reverse=True)}
                               i_aux = 0
                               new_SH = {}
                               for k,v in s_h.items():
                                   if i_aux < 5:
                                       new_SH[k] = v
                                       i_aux += 1
                                   else:
                                       break    
                               aux1=[]
                               for k in new_SH.keys():
                                    aux1.append(k)
                               index = [1,2,3,4,5]  
                               d2 = {'Degree' : aux1}
                               # Transferring d1,d2,d3,d4 into a single dictionary
                               data_Dic = dict(list(d2.items()))
                               dframe = pd.DataFrame(data_Dic,index=index)
                               st.write(dframe)
                         if selected9== 'View Centrality of all Proteins':
                               data=pd.DataFrame()
                               data['Proteins']=de1.keys()
                               data['Values']=de1.values()
                               st.dataframe(data)






                   
                     if option=='Closeness Centrality':
                         de1 = nx.closeness_centrality(G)
                         selected9 = option_menu(None, ['Top 5 Proteins','View Centrality of all Proteins'], 
    icons=['123','123'], 
    menu_icon="graph-up", default_index=0, 
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "black"},
    }
)
                         if selected9== 'Top 5 Proteins':
                               # Sorting the Dictionary of de1
                               s_h = {k: v for k, v in sorted(de1.items(),                key=lambda item: item[1], reverse=True)}
                               i_aux = 0
                               new_SH = {}
                               for k,v in s_h.items():
                                   if i_aux < 5:
                                       new_SH[k] = v
                                       i_aux += 1
                                   else:
                                       break    
                               aux1=[]
                               for k in new_SH.keys():
                                    aux1.append(k)
                               index = [1,2,3,4,5]  
                               d2 = {'Degree' : aux1}
                               # Transferring d1,d2,d3,d4 into a single dictionary
                               data_Dic = dict(list(d2.items()))
                               dframe = pd.DataFrame(data_Dic,index=index)
                               st.write(dframe)
                         if selected9== 'View Centrality of all Proteins':
                               data=pd.DataFrame()
                               data['Proteins']=de1.keys()
                               data['Values']=de1.values()
                               st.dataframe(data)









                     if option=='Betweenness Centrality':
                         de1 = nx.betweenness_centrality(G)
                         selected9 = option_menu(None, ['Top 5 Proteins','View Centrality of all Proteins'], 
    icons=['123','123'], 
    menu_icon="graph-up", default_index=0, 
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "black"},
    }
)
                         if selected9== 'Top 5 Proteins':
                               # Sorting the Dictionary of de1
                               s_h = {k: v for k, v in sorted(de1.items(),                key=lambda item: item[1], reverse=True)}
                               i_aux = 0
                               new_SH = {}
                               for k,v in s_h.items():
                                   if i_aux < 5:
                                       new_SH[k] = v
                                       i_aux += 1
                                   else:
                                       break    
                               aux1=[]
                               for k in new_SH.keys():
                                    aux1.append(k)
                               index = [1,2,3,4,5]  
                               d2 = {'Degree' : aux1}
                               # Transferring d1,d2,d3,d4 into a single dictionary
                               data_Dic = dict(list(d2.items()))
                               dframe = pd.DataFrame(data_Dic,index=index)
                               st.write(dframe)
                         if selected9== 'View Centrality of all Proteins':
                               data=pd.DataFrame()
                               data['Proteins']=de1.keys()
                               data['Values']=de1.values()
                               st.dataframe(data)

                 if selected8=="Community Detections":
                          communities = girvan_newman(G)
                          node_groups = []
                          i=1
                          for com in next(communities):
                               node_groups.append(list(com))

                          l=len(node_groups)
                          st.header('Communities : ')
                          for i in range(l):
                             da=pd.DataFrame()
                             da['community '+str(i)]=node_groups[i]
                             st.dataframe(da)



                 if selected8=="Shortest Path":
                         la=G.nodes()
                         lb=G.nodes()
                         st.header('Shortest Path Between two Proteins : ')
                         option1 = st.selectbox(
     'Source Protein ',
     la)
                         option2 = st.selectbox(
     'Target Protein ',
     lb)
                         if st.button('Find'):
                            try:        
                               l=nx.shortest_path(G,option1,option2)
                               str=''
                               for i in range(len(l)-1):
                                   str=str+l[i]+'--->'
                               str=str+l[len(l)-1]
                               abc="Shortest Path  Between "+option1+" and "+option2
                               selected = option_menu(abc, [str], 
    icons=[None], 
    menu_icon="signpost", default_index=0, 
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "black"},
    }
)
                             
                            except:
                               st.subheader('No Path Between '+option1+' and '+option2 )
                        
                         
                     











        except:
            st.image('d.png')
               





                   













          




































# UPLOAD PROTEIN
if selected2=='Upload Edge List of Protein Interactions':
     selected = option_menu("PPI NETWORK CONSTRUCTION", ['Upload Edge List of Protein Interactions'], 
    icons=['file-arrow-up'], 
    menu_icon="bezier", default_index=0, 
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "green"},
    }
)
     p1 = st.text_input('Enter Source Name : (*optional)', '  ')
     p2 = st.text_input('Enter Target Name : (*optional)', '  ')
     uploaded_file = st.file_uploader("Choose a file  (*required)")
     st.success('Note : The dataset should atleast contain two columns named Source and Target.')
     if uploaded_file is not None:
                dataframe = pd.read_csv(uploaded_file)
     selected4 = option_menu(None, ["View Uploaded Data", "Visualize Network", 
        "Statistical Analysis", 'Topological Analysis'], 
    icons=['file-bar-graph', 'bezier', "graph-up", 'graph-up'], 
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "black"},
    }
)
     if selected4=="View Uploaded Data":
         try:
                if uploaded_file is None:
                    st.error('Upload the Dataset')
                else:
                   str=p1+" - "+p2+" Protein-Protein Interaction Data"
                   st.title(str)
                   st.write(dataframe)
         except:
            st.image('d.png')
     

     if selected4=="Visualize Network":
          r='T'
          if uploaded_file is None:
              st.error('Upload the Dataset')
          else:
             list1=list(dataframe.columns)
             if 'Source' not in list1:
                  r='F'
             if 'Target' not in list1:
                  r='F'
             if r=='F':
                   st.error('A Source or Target Column is Missing from the Dataset.')
             else:
                 selected5 = option_menu(None, ["Customize Nodes", "Customize Edges", 
        "View Full Screen","Exit Full Screen"], 
    icons=['pencil', 'pencil', "fullscreen", 'fullscreen-exit'], 
    menu_icon="cast", default_index=3, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "green"},
    }
)

                 G = nx.from_pandas_edgelist(dataframe, 'Source', 'Target')
                 a='50%'
                 if selected5=="Exit Full Screen":
                    a='50%'
                 if selected5=="View Full Screen":
                    a='100%'
                 prot_net = Network(height='1000px',width=a, bgcolor='#222222', font_color='white')
                 prot_net.from_nx(G)
                 prot_net.repulsion(node_distance=420, central_gravity=0.33,
                       spring_length=110, spring_strength=0.10,
                       damping=0.95)
                 if selected5=="Customize Nodes":
                    prot_net.show_buttons(filter_=['nodes'])
                    a='50%'
                 if selected5=="Customize Edges":
                    prot_net.show_buttons(filter_=['edges'])
                    a='50%'
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
                 c1 = nx.number_of_nodes(G)
                 c2 = nx.number_of_edges(G)
                 c1="Proteins : "+str(c1)
                 c2="Interactions : "+str(c2)
                 selected = option_menu(None, ["Network Overview"], 
    icons=['lightbulb'], 
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "black"},
    }
)
                 selected = option_menu(None, [c1,c2], 
    icons=['circle','arrow-right'], 
    menu_icon="cast", default_index=-1, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#fafafa"},
    }
)





   
     # STATISTICAL ANALYSIS

     if selected4=="Statistical Analysis":
          r='T'
          if uploaded_file is None:
              st.error('Upload the Dataset')
          else:
             list1=list(dataframe.columns)
             if 'Source' not in list1:
                  r='F'
             if 'Target' not in list1:
                  r='F'
             if r=='F':
                   st.error('A Source or Target Column is Missing from the Dataset.')
             else:
                G = nx.from_pandas_edgelist(dataframe, 'Source', 'Target')
                col1,col2=st.columns(2)



                with col1:
                   selected7 = option_menu("STATISTICAL PARAMETERS", ['Number of Nodes','Number of Edges','Average Degree','Average Path Length',"Network Diameter","Network Radius","Average Clustering Coefficient",'Clustering Coefficient of each node',"Connected or Disconnected","Number of Connected Components","Center"], 
    icons=['123','123','123','123','123','123','123','123','123','123','123'], 
    menu_icon="graph-up", default_index=0, 
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa",'border': '7px solid powderblue'},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "green"},
    }
)




                with col2:
                   if selected7=="Number of Nodes":
                         c1=nx.number_of_nodes(G)
                         str= 'Number of Nodes : '+str(c1)
                         st.header(str)
                   if selected7=="Number of Edges":
                         c2=nx.number_of_edges(G)
                         str= 'Number of Edges : '+str(c2)
                         st.header(str)
                   if selected7=="Average Degree":
                         try: 
                            G_deg=nx.degree_histogram(G)
                            G_deg_sum=[a*b for a,b in zip(G_deg,range(0,len(G_deg)))]
                            avg_deg=sum(G_deg_sum)/nx.number_of_nodes(G)
                            str='Average Degree : '+str(avg_deg)
                            st.header(str)



                         except:
                             st.header('Average Degree cannot be found')

                   if selected7=="Average Path Length":
                         try:
                             c3=nx.average_shortest_path_length(G)
                             str='Average Path Length : '+str(c3) 
                             st.header(str)
                         except:
                              st.header('Average Path Length cannot be found')

                   if selected7=="Network Diameter":
                           try:
                              c4=nx.diameter(G)
                              str='Network Diameter : '+str(c4) 
                              st.header(str)
                           except:
                              st.header('Network Diameter cannot be found')
                   if selected7=="Network Radius":
                           try:
                              c5=nx.radius(G)
                              str='Network Radius : '+str(c5) 
                              st.header(str)
                           except:
                              st.header('Network Radius cannot be found')
                   if selected7=="Average Clustering Coefficient":
                           try:
                              G_cluster = sorted(list(nx.clustering(G).values()))
                              avg_clu=sum(G_cluster)/len(G_cluster)
                              str='Average Clustering Coefficient : '+str(avg_clu) 
                              st.header(str)
                           except:
                              st.header('Average Clustering Coefficient cannot be found')
                   if selected7=="Clustering Coefficient of each node":
                           try:
                              c6=nx.clustering(G)
                              new = pd.DataFrame()
                              new['nodes']=c6.keys()
                              new['values']=c6.values()
                              str='Clustering Coefficient of each node : ' 
                              st.header(str)
                              st.dataframe(new)
                           except:
                              st.header('Clustering Coefficient of each node cannot be found')
                   if selected7=="Connected or Disconnected":
                           try:
                              c7=nx.is_connected(G)
                              if c7=='True':
                                  s='Connected'
                              else:
                                  s='Disconnected'
                              str='The Network is '+s 
                              st.header(str)
                           except:
                              st.header('Connectivity cannot be found')
                   if selected7=="Number of Connected Components":
                           try:
                              c7=nx.number_connected_components(G)
                              str='Number of Connected Components : '+str(c7) 
                              st.header(str)
                           except:
                              st.header('Number of Connected Components cannot be found. Since, the graph is disconnected')
                   if selected7=="Center":
                           try:
                              c8=nx.center(G)
                              str='Center : '+str(c8) 
                              st.header(str)
                           except:
                              st.header('Center cannot be found')


    # TOPOLOGICAL ANALYSIS
     if selected4=="Topological Analysis":
          r='T'
          if uploaded_file is None:
              st.error('Upload the Dataset')
          else:
             list1=list(dataframe.columns)
             if 'Source' not in list1:
                  r='F'
             if 'Target' not in list1:
                  r='F'
             if r=='F':
                   st.error('A Source or Target Column is Missing from the Dataset.')
             else:
                G = nx.from_pandas_edgelist(dataframe, 'Source', 'Target')
                col1,col2=st.columns(2)


                with col1:
                   selected8 = option_menu("TOPOLOGICAL ANALYSIS", ['Centrality Analysis','Community Detections','Shortest Path'], 
    icons=['123','123','123'], 
    menu_icon="graph-up", default_index=0, 
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa",'border': '7px solid powderblue'},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "green"},
    }
)
              




                with col2:
                 if selected8=="Centrality Analysis":
                     option = st.selectbox(
     'Select the type of Centrality you want to Calculate',
     ('Degree Centrality', 'Closeness Centrality', 'Betweenness Centrality'))
                     if option=='Degree Centrality':
                         de1 = nx.degree_centrality(G)
                         selected9 = option_menu(None, ['Top 5 Proteins','View Centrality of all Proteins'], 
    icons=['123','123'], 
    menu_icon="graph-up", default_index=0, 
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "black"},
    }
)
                         if selected9== 'Top 5 Proteins':
                               # Sorting the Dictionary of de1
                               s_h = {k: v for k, v in sorted(de1.items(),                key=lambda item: item[1], reverse=True)}
                               i_aux = 0
                               new_SH = {}
                               for k,v in s_h.items():
                                   if i_aux < 5:
                                       new_SH[k] = v
                                       i_aux += 1
                                   else:
                                       break    
                               aux1=[]
                               for k in new_SH.keys():
                                    aux1.append(k)
                               index = [1,2,3,4,5]  
                               d2 = {'Degree' : aux1}
                               # Transferring d1,d2,d3,d4 into a single dictionary
                               data_Dic = dict(list(d2.items()))
                               dframe = pd.DataFrame(data_Dic,index=index)
                               st.write(dframe)
                         if selected9== 'View Centrality of all Proteins':
                               data=pd.DataFrame()
                               data['Proteins']=de1.keys()
                               data['Values']=de1.values()
                               st.dataframe(data)






                   
                     if option=='Closeness Centrality':
                         de1 = nx.closeness_centrality(G)
                         selected9 = option_menu(None, ['Top 5 Proteins','View Centrality of all Proteins'], 
    icons=['123','123'], 
    menu_icon="graph-up", default_index=0, 
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "black"},
    }
)
                         if selected9== 'Top 5 Proteins':
                               # Sorting the Dictionary of de1
                               s_h = {k: v for k, v in sorted(de1.items(),                key=lambda item: item[1], reverse=True)}
                               i_aux = 0
                               new_SH = {}
                               for k,v in s_h.items():
                                   if i_aux < 5:
                                       new_SH[k] = v
                                       i_aux += 1
                                   else:
                                       break    
                               aux1=[]
                               for k in new_SH.keys():
                                    aux1.append(k)
                               index = [1,2,3,4,5]  
                               d2 = {'Degree' : aux1}
                               # Transferring d1,d2,d3,d4 into a single dictionary
                               data_Dic = dict(list(d2.items()))
                               dframe = pd.DataFrame(data_Dic,index=index)
                               st.write(dframe)
                         if selected9== 'View Centrality of all Proteins':
                               data=pd.DataFrame()
                               data['Proteins']=de1.keys()
                               data['Values']=de1.values()
                               st.dataframe(data)









                     if option=='Betweenness Centrality':
                         de1 = nx.betweenness_centrality(G)
                         selected9 = option_menu(None, ['Top 5 Proteins','View Centrality of all Proteins'], 
    icons=['123','123'], 
    menu_icon="graph-up", default_index=0, 
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "black"},
    }
)
                         if selected9== 'Top 5 Proteins':
                               # Sorting the Dictionary of de1
                               s_h = {k: v for k, v in sorted(de1.items(),                key=lambda item: item[1], reverse=True)}
                               i_aux = 0
                               new_SH = {}
                               for k,v in s_h.items():
                                   if i_aux < 5:
                                       new_SH[k] = v
                                       i_aux += 1
                                   else:
                                       break    
                               aux1=[]
                               for k in new_SH.keys():
                                    aux1.append(k)
                               index = [1,2,3,4,5]  
                               d2 = {'Degree' : aux1}
                               # Transferring d1,d2,d3,d4 into a single dictionary
                               data_Dic = dict(list(d2.items()))
                               dframe = pd.DataFrame(data_Dic,index=index)
                               st.write(dframe)
                         if selected9== 'View Centrality of all Proteins':
                               data=pd.DataFrame()
                               data['Proteins']=de1.keys()
                               data['Values']=de1.values()
                               st.dataframe(data)

                 if selected8=="Community Detections":
                          communities = girvan_newman(G)
                          node_groups = []
                          i=1
                          for com in next(communities):
                               node_groups.append(list(com))

                          l=len(node_groups)
                          st.header('Communities : ')
                          for i in range(l):
                             da=pd.DataFrame()
                             da['community '+str(i)]=node_groups[i]
                             st.dataframe(da)



                 if selected8=="Shortest Path":
                         la=G.nodes()
                         lb=G.nodes()
                         st.header('Shortest Path Between two Proteins : ')
                         option1 = st.selectbox(
     'Source Protein ',
     la)
                         option2 = st.selectbox(
     'Target Protein ',
     lb)
                         if st.button('Find'):
                            try:        
                               l=nx.shortest_path(G,option1,option2)
                               str=''
                               for i in range(len(l)-1):
                                   str=str+l[i]+'--->'
                               str=str+l[len(l)-1]
                               abc="Shortest Path  Between "+option1+" and "+option2
                               selected = option_menu(abc, [str], 
    icons=[None], 
    menu_icon="signpost", default_index=0, 
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "black"},
    }
)
                             
                            except:
                               st.subheader('No Path Between '+option1+' and '+option2 )
                        

if selected1=='NCBI Organism ID Finder':
    list1=['None','Homo sapiens',
 'Saccharomyces cerevisiae',
 'Escherichia coli K12 MG1655',
 'Abiotrophia defectiva',
 'Absidia glauca',
 'Absidia repens',
 'Abyssisolibacter fermentans',
 'Acanthamoeba castellanii str. Neff',
 'Acanthocheilonema viteae',
 'Acanthochromis polyacanthus',
 'Acaricomes phytoseiuli',
 'Acaromyces ingoldii',
 'Acaryochloris marina',
 'Accipiter nisus',
 'Accumulibacter phosphatis',
 'Accumulibacter sp. BA93',
 'Acetanaerobacterium elongatum',
 'Acetitomaculum ruminis DSM 5522',
 'Acetivibrio cellulolyticus',
 'Acetivibrio ethanolgignens',
 'Acetobacter aceti',
 'Acetobacter aceti 1023',
 'Acetobacter aceti ATCC23746',
 'Acetobacter ascendens',
 'Acetobacter cibinongensis 4H-1',
 'Acetobacter ghanensis',
 'Acetobacter indonesiensis 5H-1',
 'Acetobacter malorum',
 'Acetobacter nitrogenifigens',
 'Acetobacter okinawensis',
 'Acetobacter orientalis 21F-2',
 'Acetobacter orleanensis',
 'Acetobacter oryzifermentans',
 'Acetobacter papayae JCM 25143',
 'Acetobacter pasteurianus 3P3',
 'Acetobacter pasteurianus IFO328301',
 'Acetobacter persici',
 'Acetobacter sp. 46_36',
 'Acetobacter sp. CAG:977',
 'Acetobacter syzygii 9H-2',
 'Acetobacter tropicalis',
 'Acetobacteraceae bacterium AT5844',
 'Acetobacterium bakii',
 'Acetobacterium dehalogenans DSM 11527',
 'Acetobacterium wieringae',
 'Acetobacterium woodii',
 'Acetohalobium arabaticum',
 'Acetonema longum',
 'Acetothermia bacterium 64_32',
 'Achlya hypogyna',
 'Acholeplasma axanthum',
 'Acholeplasma brassicae',
 'Acholeplasma equifetale',
 'Acholeplasma granularum',
 'Acholeplasma hippikon',
 'Acholeplasma laidlawii',
 'Acholeplasma modicum',
 'Acholeplasma multilocale ATCC 49900',
 'Acholeplasma oculi',
 'Acholeplasma palmae J233',
 'Acholeplasma sp. CAG:878',
 'Achromobacter arsenitoxydans',
 'Achromobacter denitrificans',
 'Achromobacter insolitus',
 'Achromobacter insuavis',
 'Achromobacter piechaudii ATCC43553',
 'Achromobacter piechaudii HLE',
 'Achromobacter sp. ATCC31444',
 'Achromobacter sp. DH1f',
 'Achromobacter sp. Root83',
 'Achromobacter sp. RTa',
 'Achromobacter xylosoxidans A8',
 'Achromobacter xylosoxidans NBRC15126',
 'Acidaminobacter hydrogenoformans DSM ...',
 'Acidaminococcus fermentans',
 'Acidaminococcus intestini',
 'Acidaminococcus massiliensis',
 'Acidaminococcus sp. CAG:542',
 'Acidaminococcus sp. CAG:917',
 'Acidaminococcus timonensis',
 'Acidianus hospitalis',
 'Acidianus manzaensis',
 'Acidibacillus ferrooxidans',
 'Acidiferrobacter thiooxydans',
 'Acidihalobacter ferrooxidans',
 'Acidihalobacter prosperus',
 'Acidilobus saccharovorans',
 'Acidimangrovimonas indica',
 'Acidimicrobiaceae bacterium RAAP-2',
 'Acidimicrobiia bacterium BACL6 MAG-12...',
 'Acidimicrobiia bacterium REDSEA-S09_B7',
 'Acidimicrobium ferrooxidans',
 'Acidiphilium angustum',
 'Acidiphilium cryptum',
 'Acidiphilium rubrum',
 'Acidiphilium sp. CAG:727',
 'Acidiplasma sp. MBA-1',
 'Acidithiobacillus caldus',
 'Acidithiobacillus caldus SM-1',
 'Acidithiobacillus ferrivorans',
 'Acidithiobacillus ferrooxidans ATCC23270',
 'Acidithiobacillus ferrooxidans ATCC53993',
 'Acidithiobacillus thiooxidans',
 'Acidithiobacillus thiooxidans',
 'Acidithrix ferrooxidans',
 'Acidobacteria bacterium 13_1_20CM_3_53_8',
 'Acidobacteria bacterium 13_1_40CM_2_60_7',
 'Acidobacteria bacterium 13_2_20CM_58_27',
 'Acidobacteria bacterium 28-1',
 'Acidobacteria bacterium 5-1',
 'Acidobacteria bacterium Ga0074141',
 'Acidobacteria bacterium Ga0077534',
 'Acidobacteria bacterium Ga0077551',
 'Acidobacteria bacterium KBS146',
 'Acidobacteria bacterium Mor1',
 'Acidobacteria bacterium OLB17',
 'Acidobacteria bacterium RBG_13_68_16',
 'Acidobacteria bacterium RBG_16_70_10',
 'Acidobacteria bacterium RIFCSPLOWO2_0...',
 'Acidobacteria bacterium RIFCSPLOWO2_0...',
 'Acidobacteria bacterium RIFCSPLOWO2_0...',
 'Acidobacteria bacterium RIFCSPLOWO2_1...',
 'Acidobacteria bacterium RIFCSPLOWO2_1...',
 'Acidobacteria bacterium RIFCSPLOWO2_1...',
 'Acidobacteria bacterium SCN 69-37',
 'Acidobacteriaceae bacterium KBS83',
 'Acidobacteriaceae bacterium KBS89',
 'Acidobacteriaceae bacterium KBS96',
 'Acidobacteriaceae bacterium TAA166',
 'Acidobacteriaceae bacterium URHE0068',
 'Acidobacteriales bacterium 59-55',
 'Acidobacterium capsulatum',
 'Acidobacterium sp. PMMR2',
 'Acidocella aminolytica 101 = DSM 11237',
 'Acidocella facilis',
 'Acidocella sp. MX-AZ02',
 'Acidomyces richmondensis BFW',
 'Acidothermus cellulolyticus',
 'Acidovorax caeni',
 'Acidovorax citrulli',
 'Acidovorax ebreus',
 'Acidovorax konjaci',
 'Acidovorax radicis N35',
 'Acidovorax soli',
 'Acidovorax sp. GW101-3H11',
 'Acidovorax sp. JHL-3',
 'Acidovorax sp. JHL9',
 'Acidovorax sp. JS42',
 'Acidovorax sp. KKS102',
 'Acidovorax sp. Leaf160',
 'Acidovorax sp. Leaf191',
 'Acidovorax sp. Leaf78',
 'Acidovorax sp. MRS7',
 'Acidovorax sp. RAC01',
 'Acidovorax sp. Root217',
 'Acidovorax sp. Root568',
 'Acidovorax sp. Root70',
 'Acidovorax sp. SCN 68-22',
 'Acidovorax temperans',
 'Acidovorax valerianellae',
 'Acidovorax wautersii',
 'Aciduliprofundum boonei',
 'Aciduliprofundum sp. MAR08339',
 'Acinetobacter baumannii',
 'Acinetobacter baumannii ATCC 17978',
 'Acinetobacter baumannii BJAB07104',
 'Acinetobacter baylyi',
 'Acinetobacter beijerinckii',
 'Acinetobacter beijerinckii',
 'Acinetobacter bereziniae',
 'Acinetobacter bohemicus',
 'Acinetobacter boissieri',
 'Acinetobacter bouvetii',
 'Acinetobacter bouvetii',
 'Acinetobacter brisouii',
 'Acinetobacter brisouii',
 'Acinetobacter calcoaceticus',
 'Acinetobacter calcoaceticus',
 'Acinetobacter celticus',
 'Acinetobacter defluvii',
 'Acinetobacter equi',
 'Acinetobacter gandensis',
 'Acinetobacter gerneri',
 'Acinetobacter guillouiae',
 'Acinetobacter guillouiae',
 'Acinetobacter gyllenbergii',
 'Acinetobacter gyllenbergii',
 'Acinetobacter haemolyticus',
 'Acinetobacter haemolyticus',
 'Acinetobacter harbinensis',
 'Acinetobacter indicus',
 'Acinetobacter indicus',
 'Acinetobacter johnsonii',
 'Acinetobacter johnsonii XBB1',
 'Acinetobacter junii',
 'Acinetobacter kookii',
 'Acinetobacter kyonggiensis',
 'Acinetobacter larvae',
 'Acinetobacter lwoffii',
 'Acinetobacter lwoffii NCTC 5866',
 'Acinetobacter lwoffii SH145',
 'Acinetobacter lwoffii WJ10621',
 'Acinetobacter nectaris',
 'Acinetobacter nosocomialis',
 'Acinetobacter oleivorans',
 'Acinetobacter parvus',
 'Acinetobacter pragensis',
 'Acinetobacter qingfengensis',
 'Acinetobacter radioresistens',
 'Acinetobacter radioresistens',
 'Acinetobacter rudis',
 'Acinetobacter rudis',
 'Acinetobacter schindleri',
 'Acinetobacter seohaensis',
 'Acinetobacter soli',
 'Acinetobacter sp. A47',
 'Acinetobacter sp. ADP1',
 'Acinetobacter sp. ANC 3832',
 'Acinetobacter sp. ANC 3903',
 'Acinetobacter sp. ANC 4204',
 'Acinetobacter sp. ANC 4218',
 'Acinetobacter sp. ANC 4470',
 'Acinetobacter sp. ANC 4558',
 'Acinetobacter sp. ANC 4648',
 'Acinetobacter sp. ANC 4655',
 'Acinetobacter sp. ANC 4999',
 'Acinetobacter sp. ANC 5054',
 'Acinetobacter sp. ANC 5600',
 'Acinetobacter sp. ANC3789',
 'Acinetobacter sp. ANC3862',
 'Acinetobacter sp. ANC4105',
 'Acinetobacter sp. ATCC27244',
 'Acinetobacter sp. CAG:196_36_41',
 'Acinetobacter sp. CIP 64.2',
 'Acinetobacter sp. CIP102129',
 'Acinetobacter sp. CIP56.2',
 'Acinetobacter sp. CIPA165',
 'Acinetobacter sp. DSM 11652',
 'Acinetobacter sp. HR7',
 'Acinetobacter sp. N54.MGS-139',
 'Acinetobacter sp. NCTC 7422',
 'Acinetobacter sp. NCu2D-2',
 'Acinetobacter sp. NIPH 298',
 'Acinetobacter sp. NIPH 3623',
 'Acinetobacter sp. NIPH2100',
 'Acinetobacter sp. NIPH758',
 'Acinetobacter sp. NIPH809',
 'Acinetobacter sp. NIPH899',
 'Acinetobacter sp. NIPH973',
 'Acinetobacter sp. P838',
 'Acinetobacter sp. RUH2624',
 'Acinetobacter sp. SFB',
 'Acinetobacter sp. SFD',
 'Acinetobacter sp. TGL-Y2',
 'Acinetobacter sp. TTH0-4',
 'Acinetobacter sp. Ver3',
 'Acinetobacter sp. WCHAc010034',
 'Acinetobacter tandoii',
 'Acinetobacter tjernbergiae',
 'Acinetobacter towneri',
 'Acinetobacter ursingii',
 'Acinetobacter ursingii',
 'Acinetobacter variabilis',
 'Acinetobacter venetianus',
 'Acinetobacter wuhouensis',
 'Acremonium chrysogenum ATCC 11550',
 'Acromyrmex echinatior',
 'Actibacterium atlanticum',
 'Actibacterium mucosum KCTC 23349',
 'Actinidia chinensis var. chinensis',
 'Actinoalloteichus cyanogriseus',
 'Actinoalloteichus hymeniacidonis',
 'Actinoalloteichus sp. GBA129-24',
 'Actinobacillus capsulatus',
 'Actinobacillus equuli subsp. equuli',
 'Actinobacillus minor 202',
 'Actinobacillus minor NM305',
 'Actinobacillus pleuropneumoniae 1 4074',
 'Actinobacillus pleuropneumoniae 5b L20',
 'Actinobacillus succinogenes',
 'Actinobacillus suis',
 'Actinobacteria bacterium 13_2_20CM_68_14',
 'Actinobacteria bacterium 69-20',
 'Actinobacteria bacterium casp-actino2',
 'Actinobacteria bacterium casp-actino5',
 'Actinobacteria bacterium CG2_30_50_142',
 'Actinobacteria bacterium Ga0077560',
 'Actinobacteria bacterium IMCC26207',
 'Actinobacteria bacterium IMCC26256',
 'Actinobacteria bacterium RBG_13_55_18',
 'Actinobacteria bacterium RBG_16_64_13',
 'Actinobacteria bacterium RBG_16_68_21',
 'Actinobacteria bacterium RBG_19FT_COM...',
 'actinobacterium acAMD-2',
 'actinobacterium acAMD5',
 'actinobacterium acMicro-1',
 'actinobacterium acMicro-4',
 'actinobacterium LLX17',
 'actinobacterium PHSC20C1',
 'actinobacterium SCGC AAA024-D14',
 'actinobacterium SCGC AAA027-J17',
 'actinobacterium SCGC AAA028-A23',
 'actinobacterium SCGC AAA044-D11',
 'actinobacterium SCGC AAA278-O22',
 'Actinobaculum massiliae',
 'Actinobaculum massiliense',
 'Actinobaculum schaalii',
 'Actinobaculum sp. F0552',
 'Actinobaculum suis',
 'Actinobaculum urinale',
 'Actinocatenispora sera',
 'Actinokineospora bangkokensis',
 'Actinokineospora enzanensis',
 'Actinokineospora inagensis DSM 44258',
 'Actinokineospora sp. EG49',
 'Actinokineospora terraeActinomadura atramentaria',
 'Actinomadura chibensis NBRC 106107',
 'Actinomadura flavalba',
 'Actinomadura hibisca NBRC 15177',
 'Actinomadura latina NBRC 106108',
 'Actinomadura macra NBRC 14102',
 'Actinomadura madurae',
 'Actinomadura madurae',
 'Actinomadura oligospora ATCC 43269',
 'Actinomadura rifamycini DSM 43936',
 'Actinomadura rubrobrunea NBRC 15275',
 'Actinomyces bouchesdurhonensis',
 'Actinomyces cardiffensis',
 'Actinomyces coleocanis',
 'Actinomyces dentalis',
 'Actinomyces denticolens',
 'Actinomyces europaeus',
 'Actinomyces gaoshouyii',
 'Actinomyces georgiae',
 'Actinomyces gerencseriae DSM 6844',
 'Actinomyces glycerinitolerans',
 'Actinomyces graevenitzii',
 'Actinomyces hongkongensis',
 'Actinomyces hordeovulneris',
 'Actinomyces israelii',
 'Actinomyces liubingyangii',
 'Actinomyces marimammalium',
 'Actinomyces marseillensis',
 'Actinomyces massiliensis',
 'Actinomyces massiliensis 4401292',
 'Actinomyces mediterranea',
 'Actinomyces naeslundii',
 'Actinomyces naeslundii',
 'Actinomyces nasicola',
 'Actinomyces neuii BVS029A5',
 'Actinomyces neuii DSM8576',
 'Actinomyces odontolyticus',
 'Actinomyces oris',
 'Actinomyces provencensis',
 'Actinomyces radicidentis',
 'Actinomyces ruminicola',
 'Actinomyces slackii ATCC 49928',
 'Actinomyces sp. F0310',
 'Actinomyces sp. F0311',
 'Actinomyces sp. F0330',
 'Actinomyces sp. F0332',
 'Actinomyces sp. F0337',
 'Actinomyces sp. F0384',
 'Actinomyces sp. F0386',
 'Actinomyces sp. F0400',
 'Actinomyces sp. HPA0247',
 'Actinomyces sp. ICM39',
 'Actinomyces sp. ICM47',
 'Actinomyces sp. oral taxon 414',
 'Actinomyces sp. ph3',
 'Actinomyces sp. S4C9',
 'Actinomyces sp. S6Spd3',
 'Actinomyces suimastitidis']
    selected = option_menu(None,['Organism NCBI ID Finder'], 
    icons=['patch-question'], 
    menu_icon="bezier", default_index=0, 
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "green"},
    }
)
    option3=st.multiselect('Enter Multiple Organism: ',list1)
    Entrez.email = ""
    if not Entrez.email:
       print("achup7335@gmail.com")

    taxid_list = [] 
    data_list = []
    lineage_list = []



    for species in option3:
             print ('\t'+species) # progress messages

             taxid = get_tax_id(species) # Apply your functions
             data = get_tax_data(taxid)
             lineage = {d['Rank']:d['ScientificName'] for d in data[0]['LineageEx'] if d['Rank'] in ['phylum']}

             taxid_list.append(taxid) # Append the data to lists already initiated
             data_list.append(data)
             lineage_list.append(lineage)
    if st.button('Find'):
            st.title('NCBI ID of')
            for i in range(len(taxid_list)):
                st.write(option3[i]+':'+str(taxid_list[i]))



















if selected1=='Tutorial':
    selected4 = option_menu('Tutorial', ["PPI Tutorial", "User Guide", 
        "Developer Guide"], 
    icons=['book','book','book'], 
    menu_icon="book", default_index=0, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "black"},
    }
)
    if selected4=='PPI Tutorial':
          st.title('Protein-Protein Interaction Networks')
          st.write('Protein-protein interactions (PPIs) are essential to almost every process in a cell, so understanding PPIs is crucial for understanding cell physiology in normal and disease states. It is also essential in drug development, since drugs can affect PPIs. Protein-protein interaction networks (PPIN) are mathematical representations of the physical contacts between proteins in the cell. These contacts are specific, occur between defined binding regions in the proteins and have a particular biological meaning (i.e., they serve a specific function)')
          st.write('PPI information can represent both transient and stable interactions:')
          st.write('*  Stable interactions are formed in protein complexes')
          st.write('*  Transient interactions are brief interactions that modify or carry a protein, leading to further change (e.g. protein kinases, nuclear pore importins). They constitute the most dynamic part of the interactome')
          st.write('Knowledge of PPIs can be used to:')
          st.write('*  assign putative roles to uncharacterised proteins')
          st.write('*  add fine-grained detail about the steps within a signalling pathway')
          st.write('*  characterise the relationships between proteins that form multi-molecular complexes such as the proteasome')
          st.title('Building and Analysing PPINs')
          st.write('Steps, strategies and tools used to build and analyse these networks')
          st.image('img5.png')
          st.title('Sources of PPI data')
          st.write('The first step in performing PPIN analysis is, of course, to build a network. There are different sources of PPI data that can be used to do this and it is important to be aware of their advantages and disadvantages.')
          st.write('Essentially, you can obtain PPI data from:')
          st.write('*  Your own experimental work, where you can choose how the data is represented and stored')
          st.write('*  A primary PPI database. These databases extract PPIs from the experimental evidence reported in the literature using a manual curation process. They are the primary providers of PPI data and they can represent a great deal of detail about interactions, depending on the database')
          st.write('*  A metadatabase or a predictive database. These resources bring together the information provided by different primary databases and provide a unified representation of the data to the user. Predictive databases go beyond that and use the experimentally produced datasets to computationally predict interactions in unexplored areas of the interactome. Predictive databases provide a way of broadening or refining the space of experimentally derived interactions, but the datasets produced are noisier than those from other sources')
          st.image('img6.png')
          st.title('Topological PPIN analysis')
          st.write('Analysing the topological features of a network is a useful way of identifying relevant participants and substructures that may be of biological significance. There are many different strategies that can be used to do this. In this section we focus on centrality analysis and topological clustering, although there are other strategies such as the search for shortest paths or motifs that are more often applied to networks with directionality and will not be covered here.')
          st.image('img7.png')
          st.title('Centrality analysis')
          st.write('entrality gives an estimation on how important a node or edge is for the connectivity or the information flow of the network. It is a useful parameter in signalling networks and it is often used when trying to find drug targets.')
          st.write('Centrality analysis in PPINs usually aims to answer the following question:')
          st.write('Which protein is the most important and why?')
          st.write('Edge centrality can also be analysed, but this is less common and the concepts can easily be translated from the node-based centralities, so we will focus on the latter in this section.')
          st.image('img8.png')
          st.title('Closeness Centrality')
          st.write('Closeness centrality is a useful measure that estimates how fast the flow of information would be through a given node to other nodes. Closeness centrality measures how short the shortest paths are from node i to all nodes. It is usually expressed as the normalised inverse of the sum of the topological distances in the graph (see equation at the top of Figure 28). This sum is also known as the farness of the nodes. Sometimes closeness centrality is also expressed simply as the inverse the farness (13, 14). In the example shown on the bottom half of the figure, you can see the distances matrix for the graph on the left and the calculations to get the closeness centrality on the right. Node B is the most central node according to these parameters.')
          st.image('img9.png')
          st.title('Betweenness Centrality')
          st.write('Betweenness centrality is based on communication flow. Nodes with a high betweenness centrality are interesting because they lie on communication paths and can control information flow. These nodes can represent important proteins in signalling pathways and can form targets for drug discovery. By combining this data with interference analysis we can simulate targeted attacks on protein-protein interaction networks and predict which proteins are better drug candidates, for example see Yu, et al 2007 (15).')
          st.title('Clustering Analysis')
          st.write('Looking for communities in a network is a nice strategy for reducing network complexity and extracting functional modules (e.g. protein complexes) that reflect the biology of the network. There are several terms that are commonly used when talking about clustering analysis:')
          st.image('img10.png')
    if selected4=='User Guide':
         st.title('User Guide')
         st.image('abc123.png')
         st.write('1. Click on PPI Network Construction')
         st.write('2. Click on Query a single protein. If you want to construct the PPI network of multiple proteins, Click on Query a multiple proteins. If you want to construct PPI networks by uploading datasets. Click on Upload Edge List of protein interactions.')
         st.write('3. Select protein name')
         st.write('4. Select Organism NCBI ID. NCBI ID can be founded from NCBI Organism ID Finder.')
         st.write('5. Click Get PPI data to view the PPI data')
         st.write('6. Click on Visualize network to view the PPI network')
         st.write('7. Click on Statistical Analysis to calculate statistical parameters of the network')
         st.write('7. Click on Topological Analysis to calculate centrality measures, community detection methods and shortest path on the network')

    if selected4=='Developer Guide':
        st.title('Important Source Code')
        st.write('Importing a CSV file')
        code = '''import pandas as pd
data=pd.read_csv('Filename.csv')'''
        st.code(code, language='python')
        st.write('Constructing Networks')
        code='''import networkx as nx
G1=nx.from_pandas_edgelist(dataframe, Source, Target)
nx.draw(G1, with_labels=True, node_color='blue', node_size=400, edge_color='olive', linewidths=1, font_size=15)'''
        st.code(code, language='python')
        st.write('Finding Total number of nodes and edges')
        code='''nodes=nx.number_of_nodes(G1)
edges=nx.number_of_edges(G2)'''
        st.code(code, language='python')
        st.write('calculating centrality measures')
        code='''degree=nx.degree_centrality(G1)
closeness=nx.closeness_centrality(G1)
betweenness=nx.betweenness_centrality(G1)'''
        st.code(code, language='python')
        st.write('50% Threshold calculation')
        code='''degree_threshold=max(degree.values())/2'''
        st.code(code, language='python')
        st.write('75% Threshold calculation')
        code='''degree_threshold=(max(degree.values())/4)*3'''
        st.code(code, language='python')
        st.write('Calculating Stastical Parameters')
        code='''import numpy as np
a1=np.mean([i[1] for i in G1.degree()])
b1=nx.density(G1)
c1=nx.average_clustering(G1)'''
        st.code(code, language='python')
        st.write('Finding Communities')
        code='''from networkx.algorithms.community.centrality import girvan_newman
communities=girvan_newman(G1)'''
        st.code(code, language='python')     
        st.write('Finding Shortest Paths')
        code='''path=nx.shortest_path(G1,source,target)'''
        st.code(code, language='python')
        st.write('Code to retrieve NCBI ID of an organism')
        code='''import Bio
import sys
from Bio import Entrez
def get_tax_id(species):
    """to get data from ncbi taxomomy, we need to have the taxid. we can
    get that by passing the species name to esearch, which will return
    the tax id"""
    species = species.replace(' ', "+").strip()
    search = Entrez.esearch(term = species, db = "taxonomy", retmode = "xml")
    record = Entrez.read(search)
    return record['IdList'][0]
def get_tax_data(taxid):
    """once we have the taxid, we can fetch the record"""
    search = Entrez.efetch(id = taxid, db = "taxonomy", retmode = "xml")
    return Entrez.read(search)
Entrez.email = ""
if not Entrez.email:
    print("achup7335@gmail.com")
species_list = ['Helicobacter pylori 26695', 'Thermotoga maritima MSB8', 'Deinococcus radiodurans R1', 'Treponema pallidum subsp. pallidum str. Nichols', 'Aquifex aeolicus VF5', 'Archaeoglobus fulgidus DSM 4304']

taxid_list = [] # Initiate the lists to store the data to be parsed in
data_list = []
lineage_list = []

print('parsing taxonomic data...') # message declaring the parser has begun

for species in species_list:
    print ('\t'+species) # progress messages

    taxid = get_tax_id(species) # Apply your functions
    data = get_tax_data(taxid)
    lineage = {d['Rank']:d['ScientificName'] for d in data[0]['LineageEx'] if d['Rank'] in ['phylum']}

    taxid_list.append(taxid) # Append the data to lists already initiated
    data_list.append(data)
    lineage_list.append(lineage)

print('complete!')'''
        st.code(code, language='python')
        st.write('Connecting to String database for retrieval of Protein-Protein Interactions')
        code='''import requests
import pandas as pd
protein_list = ['ACE2']
proteins = '%0d'.join(protein_list)
url = 'https://string-db.org/api/tsv/network?identifiers=' + proteins + '&species=9606'
r = requests.get(url)

lines = r.text.split('\n') # pull the text from the response object and split based on new lines
data = [l.split('\t') for l in lines] # split each line into its components based on tabs
# convert to dataframe using the first row as the column names; drop empty, final row
df = pd.DataFrame(data[1:-1], columns = data[0]) 
# dataframe with the preferred names of the two proteins and the score of the interaction
interactions = df[['preferredName_A', 'preferredName_B', 'score']]'''
        st.code(code, language='python')  


         



  

     
    
  











    
    
