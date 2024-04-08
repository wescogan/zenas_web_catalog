# Import python packages
import streamlit as st
import requests
import pandas as pd
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Zena's Amazing Athleisure Catalog")

name_on_order = st.text_input('Pick a sweatsuit color or style:')
st.write('The name on your smoothie will be:', name_on_order)

conn = st.connection("snowflake")
session = conn.session()
table = session.table("ZENAS_ATHLEISURE_DB.PRODUCTS.catalog_for_website")
my_dataframe = table# .select(col('color_or_style'))
st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

# Convert Snowpark Dataframe to Pandas Dataframe so we can use LOC function
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

color_or_style = st.selectbox(
    'Pick a sweatsuit color or style'
    , pd_df
)

caption = 'Our warm, ' + color_or_style + ' sweatsuit!'

if color_or_style:
    row = pd_df.loc[pd_df['color_or_style'] == color_or_style].iloc[0]
    st.write(row);
    #st.image(row.)
    #st.write(ingredients_list)
    #st.text(ingredients_list)
        
