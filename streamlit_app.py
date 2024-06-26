# Import python packages
import streamlit as st
import requests
import pandas as pd
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Zena's Amazing Athleisure Catalog")

conn = st.connection("snowflake")
session = conn.session()
#table = session.table("ZENAS_ATHLEISURE_DB.PRODUCTS.catalog_for_website")
#table_color_or_style = table.select(col('COLOR_OR_STYLE'))
#my_dataframe = table
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()
df = conn.query("select color_or_style from catalog_for_website;", ttl=600)
table_color_or_style = df

# Convert Snowpark Dataframe to Pandas Dataframe so we can use LOC function
# pd_df = my_dataframe.to_pandas()
# st.dataframe(pd_df)

color_or_style = st.selectbox(
    'Pick a sweatsuit color or style'
    , table_color_or_style
)

#row = pd_df.loc[pd_df['COLOR_OR_STYLE'] == color_or_style].iloc[0]
row = conn.query("select direct_url, price, size_list, upsell_product_desc from catalog_for_website where color_or_style = '" + color_or_style + "';").iloc[0]
# st.write('row:', row)

caption = 'Our warm, ' + color_or_style + ' sweatsuit!'
st.image(row.loc['DIRECT_URL'], caption)
st.write('Price:', row.loc['PRICE'])
st.write('Sizes Available:', row.loc['SIZE_LIST'])
st.write(row.loc['UPSELL_PRODUCT_DESC'])
