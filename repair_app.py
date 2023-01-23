import pandas as pd
import streamlit as st

df_item1 = pd.read_excel('repair_item1.xlsx')
df_item2 = pd.read_excel('repair_item2.xlsx')
df_chair_price = pd.read_excel('repair_price2.xlsx')

df_chair_item = pd.concat([df_item1, df_item2], join='inner')

st.set_page_config(page_title='修理見積もり')
st.markdown('#### チェア')

item_list = df_chair_item['品番'].unique()
