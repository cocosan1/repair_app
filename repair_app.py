import pandas as pd
import streamlit as st
import glob

#st
st.set_page_config(page_title='修理見積もり')
st.markdown('##### チェア修理見積もりアプリ')

df_chair_all = pd.read_excel('chair_all.xlsx')
df_base = df_chair_all.copy()

df_base['品番'] =df_base['品番'].astype(str)
df_base['タイプ'] =df_base['タイプ'].astype(str)

df_base['A-S・A・B'] = df_base['A-S・A・B'].astype(int)
df_base['C'] = df_base['C'].astype(int)
df_base['E'] = df_base['E'].astype(int)
df_base['本革A'] = df_base['本革A'].astype(int)
df_base['本革B'] = df_base['本革B'].astype(int)

# #itemファイルの読み込みconcat
# df_item1 = pd.read_excel('repair_item1.xlsx')
# df_item2 = pd.read_excel('repair_item2.xlsx')
# df_chair_item = pd.concat([df_item1, df_item2], join='inner')

# #priceファイルの読み込み
# df_chair_price = pd.read_excel('repair_price2.xlsx')

# #df_chair_price タイプstr
# df_chair_item['タイプ'] = df_chair_item['タイプ'].astype(str)
# df_chair_price['タイプ'] = df_chair_price['タイプ'].astype(str)

# #itemとpriceのmerge
# df_chair_m = df_chair_item.merge(df_chair_price, left_on='タイプ', right_on='タイプ', how='outer')
# df_chair_m.dropna(subset=['品番'], inplace=True)


# #タイプ外のconcat
# df_chair_price_nontype = pd.read_excel('repair_price2_nontype.xlsx')
# df_chair_m2 = pd.concat([df_chair_m, df_chair_price_nontype])

# df_chair_m2.to_excel('chair_all.xlsx')




#itemリストの作成
item_list = df_base['品番'].unique()
item_list2 = sorted(item_list)

#リストに1行目を挿入　すぐに見積もりが始まらないように
item_list2.insert(0, '--品番を選択--')

# *** selectbox item***
selected_item = st.sidebar.selectbox(
    '品番',
    item_list2,   
)    


if selected_item == '--品番を選択--':
#画像貼り付け
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image('img//#186.jpg', width=100, caption='#186')
        st.image('img//#736.jpg', width=100, caption='#736')
        st.image('img//#766.jpg', width=100, caption='#766')
        st.image('img//C71.jpg', width=100, caption='C71')
        st.image('img//C84.jpg', width=100, caption='C84')
        st.image('img//IS10.jpg', width=100, caption='IS10')
        st.image('img//IS20T.jpg', width=100, caption='IS20T')
        st.image('img//NW264.jpg', width=100, caption='NW264')
        st.image('img//TU10-O.jpg', width=100, caption='TU10-O')
        
    with col2:
        st.image('img//#2001-O.jpg', width=100, caption='#2001-O')
        st.image('img//#749.jpg', width=100, caption='#749')
        st.image('img//#767.jpg', width=100, caption='#767')
        st.image('img//C77.jpg', width=100, caption='C77')
        st.image('img//C91.jpg', width=100, caption='C91')
        st.image('img//IS11.jpg', width=100, caption='IS11')
        st.image('img//IS21H.jpg', width=100, caption='IS21H')
        st.image('img//NW264A.jpg', width=100, caption='NW264A')
        st.image('img//TU10-W.jpg', width=100, caption='TU10-W')

    with col3:
        st.image('img//#2001-A.jpg', width=100, caption='#2001-A')
        st.image('img//#749A.jpg', width=100, caption='#749A')
        st.image('img//#781.jpg', width=100, caption='#781')
        st.image('img//C78.jpg', width=100, caption='C78')
        st.image('img//C92.jpg', width=100, caption='C92')
        st.image('img//IS20.jpg', width=100, caption='IS20')
        st.image('img//IS22.jpg', width=100, caption='IS22')
        st.image('img//SC278.jpg', width=100, caption='SC278')
        st.image('img//TU20.jpg', width=100, caption='TU20')
        
    with col4:
        st.image('img//#726.jpg', width=100, caption='#726')
        st.image('img//#756.jpg', width=100, caption='#756')
        st.image('img//C60.jpg', width=100, caption='C60')
        st.image('img//C78T.jpg', width=100, caption='C78T')
        st.image('img//H15.jpg', width=100, caption='H15')
        st.image('img//IS20A.jpg', width=100, caption='IS20A')
        st.image('img//IS27A.jpg', width=100, caption='IS27A')
        st.image('img//SC278T.jpg', width=100, caption='SC278T')
        st.image('img//TU25.jpg', width=100, caption='TU25')

    with col5:
        st.image('img//#735.jpg', width=100, caption='#735')
        st.image('img//#756A.jpg', width=100, caption='#756A')
        st.image('img//C61.jpg', width=100, caption='C61')
        st.image('img//C81.jpg', width=100, caption='C81')
        st.image('img//H15A.jpg', width=100, caption='H15A')
        st.image('img//IS20AT.jpg', width=100, caption='IS20AT')
        st.image('img//MC12.jpg', width=100, caption='MC12')
        st.image('img//TU10-A.jpg', width=100, caption='TU10-A')
        st.image('img//TU25A.jpg', width=100, caption='TU25A')

if not selected_item == '--品番を選択--':

    col1, col2, col3 = st.columns(3)
    with col1:
        #シリーズ名の表示
        df_selected = df_base[df_base['品番']==selected_item]
        series = df_selected.iat[0, 0]
        # st.caption('シリーズ名')
        st.caption(series)

    with col2:    
        #材種の表示
        wood_name = df_selected.iat[0, 10]
        # st.markdown('###### 材種名')
        st.caption(wood_name)

    with col3:
        #imagフォルダ内のファイル名リスト取得
        files = glob.glob("img//*.jpg")
        jpg_name = f'img/{selected_item}.jpg'
        if jpg_name in files:
            st.image(f'img//{selected_item}.jpg', width=40) 

    #品番でdfの絞り込み
    df_selected = df_base[df_base['品番']==selected_item]

    #布ランクリストの作成
    df_selected2 = df_selected[['品番', '部品', 'A-S・A・B', 'C', 'E', '本革A', '本革B']]

    # *** selectbox fabrank***
    fabrank_list = df_selected2.columns[2:]
    fabrank = st.sidebar.selectbox(
        '張地ランク:',
        fabrank_list,   
    ) 

    #クッション価格一覧表示
    st.markdown('###### 張替え料金一覧')
    st.table(df_selected2)

    #修理代dict
    price_dict = {}

    #布ランクから価格の抽出
    if fabrank == 'A-S・A・B':
        fab_price = df_selected2.iat[0, 2]
    elif fabrank == 'C':
        fab_price = df_selected2.iat[0, 3]
    elif fabrank == 'E':
        fab_price = df_selected2.iat[0, 4]
    elif fabrank == '本革A':
        fab_price = df_selected2.iat[0, 5]
    elif fabrank == '本革B':
        fab_price = df_selected2.iat[0, 6] 

    price_dict['張替'] = fab_price


    #籐張り修理
    if st.sidebar.checkbox('籐張り直し修理'):
        price_tou = 24000
        price_dict['籐張替'] = price_tou
        with st.expander('■ 籐張替修理注意点'):
            st.write('現在の籐を全て剥がし、新たな籐へ張替えをさせて頂きます。')
            st.write('注）塗装は致しますが天然の籐となりますのでお持ちのものと色が変わります。')
            st.write('注）修理後は少し硬く感じますがお使い頂く中で体になじんでいきます。')

    #籐巻きなおし修理
    if st.sidebar.checkbox('籐まき直し（肘）修理　※アイガーなど'):
        price_tou2 = 6000
        price_dict['籐巻き直し'] = price_tou2

    #組み直し修理
    if st.sidebar.checkbox('組み直し修理'):
        price_kumi = 17000
        price_dict['組み直し'] = price_kumi
        with st.expander('■ 組み直し修理注意点'):
            st.write('木部の接合部分の緩みによるグラツキ等は一度部材を分解、組み直し接着をします。')
            st.write('注）接着剤が古いものはアンモニア系。現在は酢酸ビニール系で以前より丈夫です。')
            st.write('部材に破損が見られる場合は部材の修繕や交換となります。（部材代は別途）')
            st.write('注）接着剤が古いものはアンモニア系。現在は酢酸ビニール系で以前より丈夫です。')

    #座割れ修理
    if st.sidebar.checkbox('ウインザー座割れ修理'):
        price_zaware = 22000
        price_dict['座割れ修理'] = price_zaware
        with st.expander('■ 座割れ修理注意点'):
            st.write('注）座面の裏に桟を取り付ける為、事前にお伝えください。')

    #回転盤交換修理
    if st.sidebar.checkbox('ウインザー回転盤交換修理'):
        price_kaiten = 19000
        price_dict['回転盤交換'] = price_kaiten
        with st.expander('■ 回転盤交換修理注意点'):
            st.write('当時の回転盤が無いことがあるので要工場確認。（代替品対応）')
            st.write('注）回転盤の仕様が異なる場合、木部部分の削り加工が必要な場合がございます。その際はお預かり修理となります。')

    #キャスター修理
    if st.sidebar.checkbox('キャスター修理'):
        price_caster = 19000
        price_dict['キャスター修理'] = price_caster

    #Dチェア塗装
    if st.sidebar.checkbox('Dチェア再塗装'):
        price_dtosou = 25000
        price_dict['Dチェア塗装'] = price_dtosou
        with st.expander('■ 塗装修理注意点'):
            st.write('再塗装修理は現在の塗装膜を手作業で落とし、研磨後に新たな塗装をします。')
            st.write('注）色や艶を今使用している物、直した物そろえるのは難しいと事前にお伝えください。')
            st.write('注）19●●年以前のものは旧K色指定。今とは色が違います。')
            st.write('注）表面の生活傷は落ちますが、深い傷は落ちません。')
            st.write('注）研磨しますので木目が変わります。')
            st.write('注）同色での再塗装のみお受けさせて頂きます。（別色への変更不可）')
            st.write('注）同色での再塗装のみお受けさせて頂きます。（別色への変更不可）')

    #アームチェア塗装
    if st.sidebar.checkbox('アームチェア再塗装'):
        st.caption('アームのみ塗装不可')
        price_atosou = 28000
        price_dict['アームチェア塗装'] = price_atosou
        with st.expander('■ 塗装修理注意点'):
            st.write('再塗装修理は現在の塗装膜を手作業で落とし、研磨後に新たな塗装をします。')
            st.write('注）色や艶を今使用している物、直した物そろえるのは難しいと事前にお伝えください。')
            st.write('注）19●●年以前のものは旧K色指定。今とは色が違います。')
            st.write('注）表面の生活傷は落ちますが、深い傷は落ちません。')
            st.write('注）研磨しますので木目が変わります。')
            st.write('注）同色での再塗装のみお受けさせて頂きます。（別色への変更不可）')
            st.write('注）同色での再塗装のみお受けさせて頂きます。（別色への変更不可）')       


    df_price = pd.DataFrame(price_dict, index=['料金']).T
    df_price['料金'] = df_price['料金'].map(lambda x: str(x).replace(',', ''))
    df_price['料金'] = df_price['料金'].astype(int)
    df_price.loc['合計'] = df_price['料金'].sum()
    st.markdown('###### 修理料金お見積り')
    st.table(df_price)

    with st.expander('備考'):
        df_comment = pd.read_excel('comment.xlsx')
        st.markdown('###### 備考')
        df_comment['品番'] = df_comment['品番'].astype(str)
        df_comment2 = df_comment[df_comment['品番']==selected_item]
        df_comment2 = df_comment2.set_index('品番')
        st.table(df_comment2.T)

    

    # link = '[home](http://linkpagetest.s3-website-ap-northeast-1.amazonaws.com/)'
    # st.sidebar.markdown(link, unsafe_allow_html=True)
    # st.sidebar.caption('チェア画像一覧画面に戻る')     


              


