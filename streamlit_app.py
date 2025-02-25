import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
#----------------
st.set_page_config(page_title='ID Registration Dashboard')
image = Image.open('logo.jpg')
#---------------
st.image(image,
         caption='Malawi Government Cyber',
         width=140
         )
#--------------
st.title('National Registration Bureau ')
st.subheader('ID Registration Dashboard')
#--- File Upload
upload_file = st.file_uploader('Choose a XLSX file Only', type='xlsx')
if upload_file:
    st.markdown('---')
    df = pd.read_excel(upload_file, engine='openpyxl')
    st.dataframe(df)
    groupby_column = st.selectbox(
        'What to analyse :',
        ('RegID','District','Sex'),
)
      
    #---Slider
    district = df['District'].unique().tolist()
    counts = df['Count'].unique().tolist()
    col1, col2 =st.columns(2)
    count_selection = col1.slider('Registered Range:',
                                min_value = min(counts),
                                max_value = max(counts),
                                value = (min(counts),max(counts)))

    
    district_selection = col2.multiselect('District:',district,
                                        default=district)

    #----Filter slider selection
    mask = (df['Count'].between(*count_selection)) & (df['District'].isin(district_selection))
    number_of_result = df[mask].shape[0]
    st.markdown(f'*Availabe Results: {number_of_result}*')

    #---Group Dataframe
    output_columns = ['Count', 'Target']
    df_grouped = df[mask].groupby(by=[groupby_column], as_index=False)[output_columns].sum()
    df_grouped = df_grouped.reset_index()

    #---Plot Dataframe
    fig = px.bar(
        df_grouped,
        x=groupby_column,
        y='Count',
        color='Target',
        color_continuous_scale=['red','yellow','green'],
        template='plotly_white',
        title=f'<b>Registration Figures by {groupby_column}</b>'
        )
    st.plotly_chart(fig)
         
st.write('*********************************')
st.write('*developer G.Chimwaza*')
