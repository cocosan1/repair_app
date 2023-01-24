import pandas as pd
import streamlit as st

#st
st.set_page_config(page_title='修理見積もり')
st.markdown('###### チェア修理見積もり')

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

#リストに1行目を挿入　すぐに見積もりが始まらないように
item_list2.insert(0, '--品番を選択--')

# *** selectbox item***
selected_item = st.sidebar.selectbox(
    'item:',
    item_list2,   
) 

if selected_item == '--品番を選択--':
#画像貼り付け
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image('img//#2001-O.jpg', width=100, caption='#2001-O')
        st.image('img//#756A.jpg', width=100, caption='#756A')
        st.image('img//H15A.jpg', width=100, caption='H15A')
        st.image('img//TU10-A.jpg', width=100, caption='TU10-A')
    with col2:
        st.image('img//#2001-A.jpg', width=100, caption='#2001-A')
        st.image('img//766.jpg', width=100, caption='766')
        st.image('img//IS22.jpg', width=100, caption='IS22')
        st.image('img//TU10-O.jpg', width=100, caption='TU10-O')
    with col3:
        st.image('img//#749.jpg', width=100, caption='#749')
        st.image('img//767.jpg', width=100, caption='767') 
        st.image('img//IS27A.jpg', width=100, caption='IS27A')
        st.image('img//TU10-W.jpg', width=100, caption='TU10-W')
    with col4:
        st.image('img//#749A.jpg', width=100, caption='#749A')
        st.image('img//c60.jpg', width=100, caption='c60') 
        st.image('img//NW264.jpg', width=100, caption='NW264')
        st.image('img//TU25.jpg', width=100, caption='TU25')
    with col5:
        st.image('img//#756.jpg', width=100, caption='#756') 
        st.image('img//H15.jpg', width=100, caption='H15')
        st.image('img//NW264A.jpg', width=100, caption='NW264A')
        st.image('img//TU25A.jpg', width=100, caption='TU25A')

if not selected_item == '--品番を選択--':

    #品番でdfの絞り込み
    df_selected = df_chair_item[df_chair_item['品番']==selected_item]
    #修理タイプNoの抽出
    repair_num = df_selected.iat[0, 3]

    #修理タイプで修理金額dfの絞り込み
    df_price = df_chair_price[df_chair_price['タイプ']==repair_num]

    #布ランクリストの作成
    fabrank_list = df_chair_price.columns[1:-1]

    # *** selectbox fabrank***
    fabrank = st.sidebar.selectbox(
        'fabrank:',
        fabrank_list,   
    ) 

    #クッション価格一覧表示
    st.sidebar.write(df_price)

    #修理代dict
    price_dict = {}

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

    price_dict['張替'] = fab_price


    #籐張り修理
    if st.sidebar.checkbox('籐張り直し修理'):
        price_tou = 24000
        price_dict['籐張替'] = price_tou
    #籐巻きなおし修理
    if st.sidebar.checkbox('籐まき直し（肘）修理　※アイガーなど'):
        price_tou2 = 6000
        price_dict['籐巻き直し'] = price_tou2
    #組み直し修理
    if st.sidebar.checkbox('組み直し修理'):
        price_kumi = 17000
        price_dict['組み直し'] = price_kumi
    #座割れ修理
    if st.sidebar.checkbox('ウインザー座割れ修理'):
        price_zaware = 22000
        price_dict['座割れ修理'] = price_zaware
    #回転盤交換修理
    if st.sidebar.checkbox('ウインザー回転盤交換修理'):
        price_kaiten = 19000
        price_dict['回転盤交換'] = price_kaiten
    #キャスター修理
    if st.sidebar.checkbox('キャスター修理'):
        price_caster = 19000
        price_dict['キャスター修理'] = price_caster 

    df_price = pd.DataFrame(price_dict, index=['料金']).T
    df_price.loc['合計'] = df_price['料金'].sum()
    st.table(df_price)

    df_comment = pd.read_excel('C:\\Users\\SALES\\work\\git_space\\repair_app\\comment.xlsx')

    if st.sidebar.button('備考を見る'):
        st.markdown('###### 備考')
        df_comment2 = df_comment[df_comment['品番']==selected_item]
        df_comment2 = df_comment2.set_index('品番')
        st.table(df_comment2.T)
        # st.write(f'■{df_comment2.iat[0, 1]}')
        # st.write(f'■{df_comment2.iat[0, 2]}')
        # st.write(f'■{df_comment2.iat[0, 3]}')
        # st.write(f'■{df_comment2.iat[0, 4]}')
        # st.write(f'■{df_comment2.iat[0, 5]}')


              


