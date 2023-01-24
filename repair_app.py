import pandas as pd
import streamlit as st

#st
st.set_page_config(page_title='修理見積もり')
st.markdown('#### チェア')

#itemファイルの読み込みconcat
df_item1 = pd.read_excel('repair_item1.xlsx')
df_item2 = pd.read_excel('repair_item2.xlsx')
df_chair_item = pd.concat([df_item1, df_item2], join='inner')

#priceファイルの読み込み
df_chair_price = pd.read_excel('repair_price2.xlsx')

#df_chair_price タイプstr
df_chair_item['タイプ'] = df_chair_item['タイプ'].astype(str)
df_chair_price['タイプ'] = df_chair_price['タイプ'].astype(str)

#itemとpriceのmerge
df_chair_m = df_chair_item.merge(df_chair_price, left_on='タイプ', right_on='タイプ', how='outer')
df_chair_m.dropna(subset=['品番'], inplace=True)

#タイプ外のconcat
df_chair_price_nontype = pd.read_excel('repair_price2_nontype.xlsx')
df_chair_m2 = pd.concat([df_chair_m, df_chair_price_nontype])

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

#クッション価格一覧表示
st.write(df_price)

#修理代リスト
price_list = []

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

price_list.append(fab_price)

st.write(fab_price)


#籐張り修理
if st.checkbox('籐張り直し修理'):
    price_tou = 24000
    price_list.append(price_tou)
    st.write(price_tou) 
#籐巻きなおし修理
if st.checkbox('籐まき直し（肘）修理　※アイガーなど'):
    price_tou2 = 6000
    price_list.append(price_tou2)
    st.write(price_tou2)
#組み直し修理
if st.checkbox('組み直し修理'):
    price_kumi = 17000
    price_list.append(price_kumi)
    st.write(price_kumi)
#座割れ修理
if st.checkbox('ウインザー座割れ修理'):
    price_zaware = 22000
    price_list.append(price_zaware)
    st.write(price_zaware)
#回転盤交換修理
if st.checkbox('ウインザー回転盤交換修理'):
    price_kaiten = 19000
    price_list.append(price_kaiten)
    st.write(price_kaiten) 
#キャスター修理
if st.checkbox('キャスター修理'):
    price_caster = 19000
    price_list.append(price_caster)
    st.write(price_caster)                  


st.write(f'修理代合計{sum(price_list)}')

