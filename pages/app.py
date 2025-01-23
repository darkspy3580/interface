# Importing Libraries
import pandas as pd
import numpy as np
import streamlit as st
import plotly.figure_factory as ff
from plotly import graph_objs as go
import base64
import networkx as nx
import yfinance as yf
from apyori import apriori
from mlxtend.frequent_patterns import apriori, association_rules
import graphviz as graphviz
@st.cache
def convert_df(stock):
     return stock.to_csv().encode('utf-8')

def filedownload(df):
    csv=df.to_csv(index=True)
    b64=base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="df.csv">Download csv file</a>' 
    return href

stock = pd.read_csv('stock.csv')


st.image('START.png',use_column_width=True)

# SideBar Creation
st.sidebar.title('HOME')
st.sidebar.image('image3.jpg',use_column_width=True)
st.sidebar.header('SECTORAL ANALYSIS')


st.sidebar.subheader('Closing Price Analysis of Sectors')

temp=""
sect1=""

s1= st.sidebar.radio("Select",
     ('All', 'Individual'))
if s1== 'All':
     temp="ALL"
     original_title = '<p style="font-family:Arial; color:Black; font-size: 40px;"><b>CLOSING PRICE ANALYSIS</b></p>'
     st.markdown(original_title, unsafe_allow_html=True)
     fig=go.Figure()
     fig.add_trace(go.Scatter(x=stock['Date'],y=stock['Nifty Auto'],name='Nifty Auto'))
     fig.add_trace(go.Scatter(x=stock['Date'],y=stock['Nifty Bank'],name='Nifty Bank'))
     fig.add_trace(go.Scatter(x=stock['Date'],y=stock['Nifty FMCG'],name='Nifty FMCG'))
     fig.add_trace(go.Scatter(x=stock['Date'],y=stock['Nifty Health'],name='Nifty Health'))
     fig.add_trace(go.Scatter(x=stock['Date'],y=stock['Nifty Pharma'],name='Nifty Pharma'))
     fig.add_trace(go.Scatter(x=stock['Date'],y=stock['Nifty Media'],name='Nifty Media'))
     fig.add_trace(go.Scatter(x=stock['Date'],y=stock['Nifty Metal'],name='Nifty Metal'))
     fig.add_trace(go.Scatter(x=stock['Date'],y=stock['Nifty IT'],name='Nifty IT'))
     fig.add_trace(go.Scatter(x=stock['Date'],y=stock['Nifty PVT Bank'],name='Nifty PVT Bank'))
     fig.add_trace(go.Scatter(x=stock['Date'],y=stock['Nifty Realty'],name='Nifty Realty'))
     fig.add_trace(go.Scatter(x=stock['Date'],y=stock['Nifty Finance'],name='Nifty Finance'))
     fig.add_trace(go.Scatter(x=stock['Date'],y=stock['Nifty PSU Bank'],name='Nifty PSU Bank'))
     fig.layout.update(title_text="All Sectors ",xaxis_rangeslider_visible=True)
     st.plotly_chart(fig)
else:
     temp="INDIVIDUAL"
     sectors1=("Nifty Auto","Nifty Bank","Nifty FMCG","Nifty Health","Nifty Pharma","Nifty Media","Nifty Metal","Nifty IT","Nifty PVT Bank","Nifty Realty","Nifty Finance","Nifty PSU Bank")
     sect1=st.sidebar.selectbox("Select Sector : ",sectors1)
     original_title = '<p style="font-family:Arial; color:Black; font-size: 26px;"><b>Closing Price Analysis</b></p>'
     st.markdown(original_title, unsafe_allow_html=True)
     fig=go.Figure()
     fig.add_trace(go.Scatter(x=stock['Date'],y=stock[sect1],name=sect1))
     fig.layout.update(title_text=sect1,xaxis_rangeslider_visible=True)
     st.plotly_chart(fig)

if st.sidebar.button('View Sector Closing Prices'):
     st.image('image3.jpg',use_column_width=True)
     original_title = '<p style="font-family:Arial; color:Black; font-size: 26px;"><b>Sector Dataset</b></p>'
     st.markdown(original_title, unsafe_allow_html=True)
     data_load=st.text("Load Data..........")
     data_load.text("Load Data..........")
     data_load.text("Load Data..........")
     data_load.text("Loading data.........Done!")
     st.dataframe(stock)
     data_load.text(" ")
     csv = convert_df(stock)
     st.download_button(
     label="Download data as CSV",
     data=csv,
     file_name='stock.csv',
     mime='text/csv',
 )


st.sidebar.image('image3.jpg',use_column_width=True)


if st.sidebar.button('Correlated Sector'):
     st.image('image3.jpg',use_column_width=True)
     original_title = '<p style="font-family:Arial; color:Black; font-size: 40px;"><b>CORRELATED SECTOR</b></p>'
     st.markdown(original_title, unsafe_allow_html=True)
     correlations = stock.corr()
     # Transform it in a links data frame (3 columns only)
     links = correlations.stack().reset_index()
     links.columns = ['Sector_1', 'Sector_2', 'r_value']
     #Filtering the links dataframe by keeping the correlation over a threshold 0.6 and removing all self corelation.
     links1=links.loc[ (links['r_value'] > 0.6) & (links['Sector_1'] != links['Sector_2']) ]
     # Building the Graph
     G1=nx.from_pandas_edgelist(links1, 'Sector_1', 'Sector_2')
     # Plot the network
     nx.draw(G1, with_labels=True, node_color='violet', node_size=400, edge_color='black', linewidths=1, font_size=15)
     # Counting the number of nodes and edges in graph with threshold = 0.6
     count_node1_corr = nx.number_of_nodes(G1)
     count_edge1_corr = nx.number_of_edges(G1)
     # Showing Network Parameters in a data frame
     data = [['Threshold = 0.6', count_node1_corr,count_edge1_corr]]
     df = pd.DataFrame(data, columns = ['Model', 'Number of Nodes','Number of Links'])
     # Returns a Dictionary With Key as Sector and Value as the Centrality Values
     de1 = nx.degree_centrality(G1)
     c1 = nx.closeness_centrality(G1)
     b1 = nx.betweenness_centrality(G1)
     e1 = nx.eigenvector_centrality(G1)
     s_h = {k: v for k, v in sorted(e1.items(), key=lambda item: item[1], reverse=True)}
     i_aux = 0
     new_SH = {}
     for k,v in s_h.items():
         if i_aux < 10:
             new_SH[k] = v
             i_aux += 1
         else:
             break
     aux1=[]
     for k in new_SH.keys():
          aux1.append(k) 
     d1 = {'Eigenvector' : aux1}

     s_h = {k: v for k, v in sorted(de1.items(), key=lambda item: item[1], reverse=True)}
     i_aux = 0
     new_SH = {}
     for k,v in s_h.items():
          if i_aux < 10:
               new_SH[k] = v
               i_aux += 1
          else:
               break
     aux1=[]
     for k in new_SH.keys():
          aux1.append(k)
     index = [1,2,3,4,5,6,7,8,9,10]  
     d2 = {'Degree' : aux1}
     s_h = {k: v for k, v in sorted(c1.items(), key=lambda item: item[1], reverse=True)}
     i_aux = 0
     new_SH = {}
     for k,v in s_h.items():
        if i_aux < 10:
           new_SH[k] = v
           i_aux += 1
        else:
           break
     aux1=[]
     for k in new_SH.keys():
         aux1.append(k)
     d3 = {'Closeness' : aux1}
     s_h = {k: v for k, v in sorted(b1.items(), key=lambda item: item[1], reverse=True)}
     i_aux = 0
     new_SH = {}
     for k,v in s_h.items():
          if i_aux < 10:
              new_SH[k] = v
              i_aux += 1
          else:
              break
     aux1=[]
     for k in new_SH.keys():
           aux1.append(k)
     d4 = {'Betweenness' : aux1}
     data_Dic = dict(list(d1.items())+list(d2.items())+list(d3.items())+list(d4.items()))
     dframe = pd.DataFrame(data_Dic,index=index)
     if temp=="ALL":
         st.write("Correlation of All Sectors")
         st.bar_chart(correlations)
         abc=dframe.head(1)
         original_title = '<p style="font-family:Arial; color:Black; font-size: 26px;"><b>Results Using Network Centrality Measures</b></p>'
         st.markdown(original_title, unsafe_allow_html=True)
         st.write(abc)
         
         original_title = '<p style="font-family:Arial; color:Black; font-size: 18px;"><b>Nifty Auto is the Most Correlated Sector</b></p>'
         st.markdown(original_title, unsafe_allow_html=True)
     else:
         st.write("Correlation of ",sect1)
         st.bar_chart(correlations[sect1])
        

st.sidebar.image('image3.jpg',use_column_width=True)


if st.sidebar.button('Influenced Sector'):
     st.image('image3.jpg',use_column_width=True)
     original_title = '<p style="font-family:Arial; color:Black; font-size: 40px;"><b>INFLUENCED SECTOR</b></p>'
     st.markdown(original_title, unsafe_allow_html=True)
     stock = stock.iloc[: , 1:]
     length=len(stock)
     for j in range(0,12):
        for i in range(0,length-1):
           if stock.values[i+1,j]>stock.values[i,j] :
              stock.values[i,j]=1
           else :
              stock.values[i,j]=0
     stock = stock.iloc[:-1]
     frequent_patterns=apriori(stock,min_support=0.01,max_len=2,use_colnames=True)
     rules=association_rules(frequent_patterns,metric="confidence",min_threshold=0.5)
     # Changing the antecedents and consequents values from frozenset to list
     rules["antecedents"] = rules["antecedents"].apply(lambda x: list(x)[0]).astype("unicode")
     rules["consequents"] = rules["consequents"].apply(lambda x: list(x)[0]).astype("unicode")
     apriori_rules = pd.DataFrame([rules.antecedents, rules.consequents, rules.confidence]).transpose()
     apriori_filtered1 =apriori_rules.loc[ (apriori_rules['confidence'] > 0.7)]
     # Building the Graph
     G1=nx.from_pandas_edgelist(apriori_filtered1, 'antecedents', 'consequents', create_using=nx.DiGraph() )
     # Plot the Network
     nx.draw(G1,with_labels=True, node_color='yellow', node_size=400, edge_color='black', linewidths=1, font_size=10, arrows=True)
     # Returns a Dictionary With Key as Sector and Value as the Centrality Values
     de1 = nx.degree_centrality(G1)
     c1 = nx.closeness_centrality(G1)
     b1 = nx.betweenness_centrality(G1)
     e1 = nx.eigenvector_centrality(G1)
     s_h = {k: v for k, v in sorted(e1.items(), key=lambda item: item[1], reverse=True)}
     i_aux = 0
     new_SH = {}
     for k,v in s_h.items():
         if i_aux < 10:
             new_SH[k] = v
             i_aux += 1
         else:
             break
     aux1=[]
     for k in new_SH.keys():
          aux1.append(k) 
     d1 = {'Eigenvector' : aux1}

     s_h = {k: v for k, v in sorted(de1.items(), key=lambda item: item[1], reverse=True)}
     i_aux = 0
     new_SH = {}
     for k,v in s_h.items():
          if i_aux < 10:
               new_SH[k] = v
               i_aux += 1
          else:
               break
     aux1=[]
     for k in new_SH.keys():
          aux1.append(k)
     index = [1,2,3,4,5,6,7,8,9,10]  
     d2 = {'Degree' : aux1}
     s_h = {k: v for k, v in sorted(c1.items(), key=lambda item: item[1], reverse=True)}
     i_aux = 0
     new_SH = {}
     for k,v in s_h.items():
        if i_aux < 10:
           new_SH[k] = v
           i_aux += 1
        else:
           break
     aux1=[]
     for k in new_SH.keys():
         aux1.append(k)
     d3 = {'Closeness' : aux1}
     s_h = {k: v for k, v in sorted(b1.items(), key=lambda item: item[1], reverse=True)}
     i_aux = 0
     new_SH = {}
     for k,v in s_h.items():
          if i_aux < 10:
              new_SH[k] = v
              i_aux += 1
          else:
              break
     aux1=[]
     for k in new_SH.keys():
           aux1.append(k)
     d4 = {'Betweenness' : aux1}
     data_Dic = dict(list(d1.items())+list(d2.items())+list(d3.items())+list(d4.items()))
     dframe = pd.DataFrame(data_Dic,index=index)
     abc=dframe.head(1)
     original_title = '<p style="font-family:Arial; color:Black; font-size: 26px;"><b>Results Using Network Centrality Measures</b></p>'
     st.markdown(original_title, unsafe_allow_html=True)
     st.write(abc)
         
     original_title = '<p style="font-family:Arial; color:Black; font-size: 18px;"><b>Nifty Auto is the Most Influenced Sector</b></p>'
     st.markdown(original_title, unsafe_allow_html=True)
     


st.sidebar.image('image3.jpg',use_column_width=True)
st.sidebar.header('STOCK PREDICTION')
stock1=('^NSEI',"HCLTECH.NS","TECHM.NS","SUNPHARMA.NS",'ASIANPAINT.NS','ULTRACEMCO.NS','NTPC.NS','TITAN.NS','COALINDIA.NS','TATAMOTORS.NS','BPCL.NS','LT.NS','ONGC.NS','EICHERMOT.NS','SHREECEM.NS','IOC.NS','RELIANCE.NS','DIVISLAB.NS','HINDALCO.NS','BRITANNIA.NS','TATACONSUM.NS','ITC.NS','INFY.NS','GRASIM.NS','SBILIFE.NS','WIPRO.NS','ADANIPORTS.NS','HEROMOTOCO.NS','NESTLEIND.NS','HDFCLIFE.NS','WIPRO.NS','BAJAJ-AUTO.NS',' SHREECEM.NS','BHARTIARTL.NS','NTPC.NS','MARUTI.NS','LT.NS','CIPLA.NS','RELIANCE.NS','KOTAKBANK.NS','ULTRACEMCO.NS','TCS.NS','GRASIM.NS','INDUSINDBK.NS','TATASTEEL.NS','ICICIBANK.NS','BAJFINANCE.NS','COALINDIA.NS','MM.NS','BAJAJFINSV.NS')
stock2=st.sidebar.selectbox("Select Stock for prediction : ",stock1)
if st.sidebar.button('Predict'):
    yf.pdr_override()    
    st.image('image3.jpg',use_column_width=True)
    original_title = '<p style="font-family:Arial; color:Black; font-size: 40px;"><b>STOCK PREDICTION </b></p>'
    st.markdown(original_title, unsafe_allow_html=True)
    original_title = '<p style="font-family:Arial; color:Black; font-size: 26px;"><b>Historical Data</b></p>'
    st.markdown(original_title, unsafe_allow_html=True)
    st.write("Historical data of ",stock2," from January 2010 to December 2019")
    data_load=st.text("Load Data..........")
    data_load.text("Load Data..........")
    data_load.text("Load Data..........")
    df = yf.download(stock2, "2010-01-01", "2019-12-31")
    data_load.text("Loading data.........Done!")
    st.write(df)
    data_load.text(" ")
    st.markdown(filedownload(df),unsafe_allow_html=True)
    df['Date'] = df.index
    
    #Analyze the Data
    original_title = '<p style="font-family:Arial; color:Black; font-size: 26px;"><b>Analyzing the Closing and Opening Price of Stock</b></p>'
    st.markdown(original_title, unsafe_allow_html=True)
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'],y=df['Close'],name='Stock Closing Price'))
    fig.add_trace(go.Scatter(x=df['Date'],y=df['Open'],name='Stock Opening Price'))
    fig.layout.update(title_text=stock2,xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

    mx=df['Close'].max()
    r1=round(mx, 2)
    mn=df['Close'].min()
    r2=round(mn, 2)
    col1, col2 = st.columns(2)
    col1.metric("Highest Price", r1)
    col2.metric("Lowest Price", r2)
    
    data = df.filter(['Close'])
    #Convert the dataframe to a numpy array
    dataset = data.values
    #Get the number of rows to train the model on
    training_data_len = int(np.ceil( len(dataset) * .8 ))


    from sklearn.preprocessing import MinMaxScaler

    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(dataset)

    train_data = scaled_data[0:int(training_data_len), :]
    #Split the data into x_train and y_train data sets
    x_train = []
    y_train = []

    for i in range(60, len(train_data)):
        x_train.append(train_data[i-60:i, 0])
        y_train.append(train_data[i, 0])

    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    from keras.models import Sequential
    from keras.layers import Dense, LSTM

    #Build the LSTM model
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape= (x_train.shape[1], 1)))
    model.add(LSTM(50, return_sequences= False))
    model.add(Dense(25))
    model.add(Dense(1))
    
    model.compile(optimizer='adam',loss='mean_squared_error')
    model.fit(x_train,y_train,batch_size=1,epochs=1)

    test_data=scaled_data[training_data_len-60:,:]  
    #Create the data sets x_test and y_test
    x_test = []
    y_test = dataset[training_data_len:, :]
    for i in range(60, len(test_data)):
        x_test.append(test_data[i-60:i, 0]) 

    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1 ))
    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)
    rmse = np.sqrt(np.mean(((predictions - y_test) ** 2)))
    
    train = data[:training_data_len]
    valid = data[training_data_len:]
    valid['Predictions'] = predictions
    

    original_title = '<p style="font-family:Arial; color:Black; font-size: 26px;"><b>Prediction Using LSTM</b></p>'
    st.markdown(original_title, unsafe_allow_html=True)
    fig=go.Figure()
    fig.add_trace(go.Scatter(y=valid['Close'],name='Orginal Price'))
    fig.add_trace(go.Scatter(y=valid['Predictions'],name='Predicted Price'))
    fig.layout.update(title_text=stock2,xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)




st.sidebar.image('image3.jpg',use_column_width=True)
if st.sidebar.button('About Us'):
    original_title = '<p style="font-family:Arial; color:Black; font-size: 40px;"><b>ABOUT US </b></p>'
    st.markdown(original_title, unsafe_allow_html=True)
    st.image('image3.jpg',use_column_width=True)
    with st.expander("About NSE India"):
        st.image('image3.jpg',use_column_width=True)
        st.write('''National Stock Exchange of India Limited (NSE) is the leading stock exchange of 
India, located in Mumbai, Maharashtra. It is under the ownership of some leading
financial institutions, banks, and insurance companies.[5] NSE was established 
in 1992 as the first dematerialized electronic exchange in the country. NSE was the 
first exchange in the country to provide a modern, fully automated screen-based 
electronic trading system that offered easy trading facilities to investors spread 
across the length and breadth of the country. Vikram Limaye is the Managing Director 
and Chief Executive Officer of NSE.''')
    with st.expander("About Sectors"):
           st.image('image3.jpg',use_column_width=True)
           st.write('1.  **NIFTY AUTO :** This sector includes manufacturers of cars & motorcycles, heavy vehicles, auto ancillaries, tyres, etc.')
           st.write('2.  **NIFTY BANK :** This sector represents 12 most liquid and large capitalised stocks from the banking sector which trade on the National Stock Exchange (NSE).')
           st.write('3. **NIFTY FINANCE :** The Nifty Financial Services Index is designed to reflect the behaviour and performance of the Indian financial market which includes banks, financial institutions, housing finance, insurance companies and other financial services companies.')
           st.write('4. **NIFTY FMCG :** This sector includes goods and products, which are non-durable, mass-consumption products and available off the shelf.')
           st.write('5. **NIFTY HEALTHCARE :** This sector is designed to reflect the behaviour and performance of the Healthcare companies.')
           st.write('6. **NIFTY IT :** This sector is designed to reflect the behaviour of companies engaged into activities such as IT infrastructure, IT education and software training, networking infrastructure, software development, hardware, IT support and maintenance etc...')
           st.write('7. **NIFTY MEDIA :** This sector is designed to reflect the behavior and performance of sectors such as media & entertainment,  printing and publishing. ')
           st.write(' 8. **NIFTY METAL :** This sector is designed to reflect the behavior and performanceof the metals sector including mining.')
           st.write(' 9. **NIFTY PHARMA :** This sector is designed to reflect the behavior and performance of the companies that are engaged into manufacturing of pharmaceuticals. ')
           st.write('10. **NIFTY PRIVATE BANK :** This sector is designed to reflect the behavior and performance of the banks from private sector.')
           st.write('11. **NIFTY PSU BANK :** The NIFTY PSU Bank Index captures the performance of the PSU Banks. All Public Sector Banks that are traded  at the National Stock Exchange (NSE) are eligible for inclusion in the index subject to fulfilment of other inclusion criteria namely listing history and trading frequency.')
           st.write('12. **NIFTY REALTY :** This sector is designed to reflect the behavior and performance of the companies that are engaged into construction of residential & commercial real estate properties')
           


if st.sidebar.button('Contact Us'):
    original_title = '<p style="font-family:Arial; color:Black; font-size: 40px;"><b>CONTACT US </b></p>'
    st.markdown(original_title, unsafe_allow_html=True)
    st.image('image3.jpg',use_column_width=True)
    st.write("jisharc@gmail.com")
    st.write("achup@gmail.com")
    st.write("ashish@gmail.com")
    st.write("hari@gmail.com")
    st.write("hareendran@gmail.com")
    st.write("midhun@gmail.com")
st.image('END.png',use_column_width=True)

