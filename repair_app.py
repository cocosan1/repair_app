import pandas as pd
import streamlit as st

#itemファイルの読み込みconcat
df_item1 = pd.read_excel('repair_item1.xlsx')
df_item2 = pd.read_excel('repair_item2.xlsx')
df_chair_item = pd.concat([df_item1, df_item2], join='inner')

#priceファイルの読み込み
df_chair_price = pd.read_excel('repair_price2.xlsx')

#df_chair_price タイプstr
df_chair_price['タイプ'] = df_chair_price['タイプ'].astype(str)

#st
st.set_page_config(page_title='修理見積もり')
st.markdown('#### チェア')

#itemリストの作成
item_list = df_chair_item['品番'].unique()
item_list2 = sorted(item_list)

# *** selectbox item***
selected_item = st.selectbox(
    'item:',
    item_list2,   
) 

#品番でdfの絞り込み
df_selected = df_chair_item[df_chair_item['品番']==selected_item]
#修理タイプNoの抽出
repair_num = df_selected.iat[0, 3]

#修理タイプで修理金額dfの絞り込み
df_price = df_chair_price[df_chair_price['タイプ']==repair_num]

#布ランクリストの作成
fabrank_list = df_chair_price.columns[1:-1]

# *** selectbox fabrank***
fabrank = st.selectbox(
    'fabrank:',
    fabrank_list,   
) 

#布ランクから価格の抽出
if fabrank == 'A-S・A・B':
    fab_price = df_price.iat[0, 1]
elif fabrank == 'C':
    fab_price = df_price.iat[0, 2]
elif fabrank == 'E':
    fab_price = df_price.iat[0, 3]
elif fabrank == '本革A':
    fab_price = df_price.iat[0, 4]
elif fabrank == '本革B':
    fab_price = df_price.iat[0, 5]      

st.write(df_price)
st.write(fab_price)

