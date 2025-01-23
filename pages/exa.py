import streamlit as st
from streamlit_option_menu import option_menu



def func2():
            st.title('Protein-Protein Interaction Network')
            original_title = '<p style="font-family:Arial; color:#37333F; font-size: 18px;"><b>Protein-protein interactions (PPIs) are essential to almost every process in a cell, so understanding PPIs is crucial for understanding cell physiology in normal and disease states.It is the Lasting and specific physical contacts established between two or more proteins for carried out some specific biological activity. It Represents pair wise protein interactions of the organisms. It is also essential in drug development, since drugs can affect PPIs. PPI information can represent both transient and stable interactions. Stable interactions are formed in protein complexes (e.g. ribosome, haemoglobin).</b></p>'
            st.markdown(original_title, unsafe_allow_html=True)


def func1():
            st.title('What is a Protein?')
            original_title = '<p style="font-family:Arial; color:#37333F; font-size: 18px;"><b>Protein are large biomolecules that consisting of one or more long chains of amino acids. A protein contains at least one long polypeptide( chain of amino acids). Primarily the sequence of amino acid differs the protein from each other.</b></p>'
            st.markdown(original_title, unsafe_allow_html=True)
            st.title('What are Amino-Acids and Polypeptide?')
            original_title = '<p style="font-family:Arial; color:#37333F; font-size: 18px;"><b>Amino  acid  are  biologically  important  organic  compound  that consists of </b></p>'
            st.markdown(original_title, unsafe_allow_html=True)
            original_title = '<p style="font-family:Arial; color:#37333F; font-size: 18px;"><b>>>>> Amine group[ -NH(2)]</b></p>'
            st.markdown(original_title, unsafe_allow_html=True)
            original_title = '<p style="font-family:Arial; color:#37333F; font-size: 18px;"><b>>>>> Carboxylic Acid group[ -COOH]</b></p>'
            st.markdown(original_title, unsafe_allow_html=True)
            original_title = '<p style="font-family:Arial; color:#37333F; font-size: 18px;"><b>>>>> and a side chain[ -R]</b></p>'
            st.markdown(original_title, unsafe_allow_html=True)
            st.image('img1.png')
            original_title = '<p style="font-family:Arial; color:#37333F; font-size: 18px;"><b>Therefore  the  key  elements  of  amino  acid  are  carbon(C)  , hydrogen(H) , oxygen(O) and nitrogen(N).</b></p>'
            st.markdown(original_title, unsafe_allow_html=True)
            original_title = '<p style="font-family:Arial; color:#37333F; font-size: 18px;"><b>When two or more amino acid is connected through peptide bond it is called polypeptide(amino acid chain).</b></p>'
            st.markdown(original_title, unsafe_allow_html=True)
            st.image('img2.png')
            st.title('Protein Structure')
            original_title = '<p style="font-family:Arial; color:#37333F; font-size: 18px;"><b>Protein structure is the three­ dimensional arrangement of atoms in a protein molecule. To perform several biological functions, protein folds into one or more specific spatial conformations. Several non­covalent interactions are responsible for this confirmations. Levels of Protein Structures are :</b></p>'
            st.markdown(original_title, unsafe_allow_html=True)
            original_title = '<p style="font-family:Arial; color:#37333F; font-size: 18px;"><b>>>>> Primary Structure: </b></p>'
            st.markdown(original_title, unsafe_allow_html=True)
            st.write('Linear sequence of amino acids in the polypeptide chain.')
            original_title = '<p style="font-family:Arial; color:#37333F; font-size: 18px;"><b>>>>> Secondary Structure: </b></p>'
            st.markdown(original_title, unsafe_allow_html=True)
            st.write('Helical structure due to hydrogen bond between the main-chain peptide groups.')
            original_title = '<p style="font-family:Arial; color:#37333F; font-size: 18px;"><b>>>>> Tertiary Structure: </b></p>'
            st.markdown(original_title, unsafe_allow_html=True)
            st.write('Folded into a compact globular structure due to hydrophobic interactions.')
            st.title('Central Dogma')
            original_title = '<p style="font-family:Arial; color:#37333F; font-size: 18px;"><b>Explains the flow of genetic information from DNA to RNA, to make a functional product Protein.</b></p>'
            st.markdown(original_title, unsafe_allow_html=True)
            original_title = '<p style="font-family:Arial; color:#37333F; font-size: 18px;"><b>Stages of Central Dogma:</b></p>'
            st.markdown(original_title, unsafe_allow_html=True)
            original_title = '<p style="font-family:Arial; color:#37333F; font-size: 18px;"><b>>>>>Replication: Fundamental step of central dogma, make a new DNA from existing DNA by DNA polymerase.</b></p>'
            st.markdown(original_title, unsafe_allow_html=True)
            original_title = '<p style="font-family:Arial; color:#37333F; font-size: 18px;"><b>Transcription: Make new mRNA from DNA by RNA polymerase.</b></p>'
            st.markdown(original_title, unsafe_allow_html=True)
            original_title = '<p style="font-family:Arial; color:#37333F; font-size: 18px;"><b>Translation: Make new protein from mRNA by ribosome.</b></p>'
            st.markdown(original_title, unsafe_allow_html=True)
            st.image('img3.png')

st.set_page_config(page_title='PPINA : Protein-Protein Interaction Network Analysis', page_icon='a.jpg',layout="wide")










    


































str=0
with st.sidebar:
    if st.button('Tutorial'):
        str=1

if str==1:
    selected20 = option_menu("TUTORIAL", ["Protein-Protein Interaction Notes", 'App User Guide','Developer Guide'], 
    icons=['book-half', 'journals','journal-code'], 
    menu_icon="book", default_index=0, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "17px"}, 
        "nav-link": {"font-size": "17px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "green"},
    }
)

 
    if selected20=='Protein-Protein Interaction Notes':
        selected21 = option_menu(None, ['Introduction','Protein-Protein Interaction Network'], 
    icons=['book-half','book-half'], 
    menu_icon="book", default_index=0,
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "17px"}, 
        "nav-link": {"font-size": "17px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "black"},
    }
)

        if selected21=='Introduction':
                func1()
                if st.button('NEXT : Protein-Protein Interaction Network'):
                      func2()

        if selected21=='Protein-Protein Interaction Network':
                func2()



 


    if selected20=='App User Guide':
        st.write('a')

    if selected20=='Developer Guide':
        st.write('a')
        

   