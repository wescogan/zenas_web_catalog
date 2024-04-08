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
my_dataframe = session.table("ZENAS_ATHLEISURE_DB.PRODUCTS.catalog_for_website").select(col('color_or_style'))
st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

# Convert Snowpark Dataframe to Pandas Dataframe so we can use LOC function
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

color_or_style = st.selectbox(
    'Pick a sweatsuit color or style'
    , my_dataframe
)

caption = 'Our warm, ' + color_or_style + ' sweatsuit!'

if color_or_style:
    st.image(
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        
        st.subheader(fruit_chosen + ' Nutritional Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + search_on)
        fv_dv = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
    
    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                values ('""" + ingredients_string + """','""" + name_on_order + """ ')"""

    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button('Submit order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered, ' + name_on_order +  '!', icon="✅")
        
