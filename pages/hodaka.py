import pandas as pd
import streamlit as st
import webbrowser
import glob
from PIL import Image

#st
st.set_page_config(page_title='修理見積もり')
st.markdown('#### 穂高見積もりアプリ')

df_hk = pd.read_excel('hk0.xlsx')
df_base = df_hk.copy()

df_base['A-S'] = df_base['A-S'].astype(str)
df_base['A'] = df_base['A'].astype(str)
df_base['B'] = df_base['B'].astype(str)
df_base['C'] = df_base['C'].astype(str)
df_base['E'] = df_base['E'].astype(str)
df_base['本革A'] = df_base['本革A'].astype(str)
df_base['本革B'] = df_base['本革B'].astype(str)

df_base['A-S'] = df_base['A-S'].map(lambda x: x.replace(',', ''))
df_base['A'] = df_base['A'].map(lambda x: x.replace(',', ''))
df_base['B'] = df_base['B'].map(lambda x: x.replace(',', ''))
df_base['C'] = df_base['C'].map(lambda x: x.replace(',', ''))
df_base['E'] = df_base['E'].map(lambda x: x.replace(',', ''))
df_base['本革A'] = df_base['本革A'].map(lambda x: x.replace(',', ''))
df_base['本革B'] = df_base['本革B'].map(lambda x: x.replace(',', ''))

df_base['A-S'] = df_base['A-S'].astype(int)
df_base['A'] = df_base['A'].astype(int)
df_base['B'] = df_base['B'].astype(int)
df_base['C'] = df_base['C'].astype(int)
df_base['E'] = df_base['E'].astype(int)
df_base['本革A'] = df_base['本革A'].astype(int)
df_base['本革B'] = df_base['本革B'].astype(int)

#itemリストの作成
item_list = df_base['品番'].unique()
item_list2 = sorted(item_list)

#リストに1行目を挿入　すぐに見積もりが始まらないように
item_list2.insert(0, '--品番を選択--')


# *** selectbox item***
st.sidebar.markdown('#### 穂高見積')
selected_item = st.sidebar.selectbox(
    '品番:',
    item_list2,   
)    


if selected_item == '--品番を選択--':
    col1, col2 = st.columns(2)
    with col1:
        img_hk = Image.open('img/hodaka-fig02.jpg')
        st.image(img_hk)
        st.caption('No6/Hk255')

    with col2:
        img_6so = Image.open('img/6so_comment.JPG')
        st.image(img_6so)
        st.caption('6W/6SO')

    cola, colb, colc = st.columns(3)
    with cola:
        img_suberi = Image.open('img/S_クッション滑り止めシート.jpg')
        st.image(img_suberi, width=150)
        st.caption('クッション滑り止めシート')

    with colb:
        img_suberiband = Image.open('img/S_クッション止めバンド２ケ.jpg')
        st.image(img_suberiband, width=150)
        st.caption('クッション滑り止めバンド')

    with colc:
        img_renketu = Image.open('img/S_連結マジックバンド.jpg')
        st.image(img_renketu, width=150)
        st.caption('連結マジックバンド')    



if not selected_item == '--品番を選択--':

    #品番でdfの絞り込み
    df_selected = df_base[df_base['品番']==selected_item]

    #布ランクリストの作成
    df_selected2 = df_selected[['品番', '部品', 'A-S', 'A', 'B', 'C', 'E', '本革A', '本革B']]

    #****************ランク　入力フォーム*******************
    # *** selectbox fabrank***
    fabrank_list = df_selected2.columns[2:]
    fabrank_list2 = fabrank_list.insert(0, '--張地ランクを選択--')

    fabrank = st.sidebar.selectbox(
        '張地ランク:',
        fabrank_list2,   
    ) 

    if fabrank == '--張地ランクを選択--':
         #クッション価格一覧表示
        st.markdown('###### 張替え料金一覧')
        st.table(df_selected2)
    else:
        col01, col02 = st.columns(2)
        with col01:
            st.write(f'◆品番: {selected_item}') 
        with col02:
            st.write(f'◆張地ランク: {fabrank}') 

        st.write('サイドバーの選択フォームから選択してください')  


    # 布ランクからdfの抽出
    if fabrank == 'A-S':
        df_selected2_rank = df_selected2.iloc[:, [0, 1, 2]]
    elif fabrank == 'A':
        df_selected2_rank = df_selected2.iloc[:, [0, 1, 3]]
    elif fabrank == 'B':
        df_selected2_rank= df_selected2.iloc[:, [0, 1, 4]]        
    elif fabrank == 'C':
        df_selected2_rank = df_selected2.iloc[:, [0, 1, 5]]
    elif fabrank == 'E':
        df_selected2_rank = df_selected2.iloc[:, [0, 1, 6]]
    elif fabrank == '本革A':
        df_selected2_rank = df_selected2.iloc[:, [0, 1, 7]]
    elif fabrank == '本革B':
        df_selected2_rank = df_selected2.iloc[:, [0, 1, 8]]

    name_list = []
    price_list = []
    num_list = []

    #****************メイン入力フォーム*******************
    with st.sidebar.form(key='form0'):

        st.markdown('#### 計算ボタン')
        submitted0 = st.form_submit_button('計算')    

        #*************部品1*****************************

        st.markdown('#### 部品選択フォーム')
        # 部品リスト作成
        parts_list = df_selected2['部品'].unique()
        parts_list = list(parts_list) #np arrayからlistへ
        parts_list.insert(0, '') 

        # *** selectbox 項目1***
        parts1 = st.selectbox(
            '■ 部品1',
            parts_list,   
        ) 
        
        cont1 = st.number_input('数量入力', min_value=0, max_value=10, key='cont1')

        if parts1 != '':
            #部品名/単価/数量をリストに追加
            df_p1 = df_selected2_rank[df_selected2_rank['部品']==parts1]
            price1 = df_p1.iat[0, 2]

            name_list.append(parts1)
            price_list.append(price1)
            num_list.append(cont1)

        #*************部品2****************************
    
        parts2 = st.selectbox(
            '■ 部品2',
            parts_list,   
        ) 
        # *** selectbox 項目1***
        cont2 = st.number_input('数量入力', min_value=0, max_value=10, key='cont2')

        if parts2 != '':
            #部品名/単価/数量をリストに追加
            df_p2 = df_selected2_rank[df_selected2_rank['部品']==parts2]
            price2 = df_p2.iat[0, 2]

            name_list.append(parts2)
            price_list.append(price2)
            num_list.append(cont2)

        #*************部品3*****************************
    
        parts3 = st.selectbox(
            '■ 部品3',
            parts_list,   
        ) 
        # *** selectbox 項目1***
        cont3 = st.number_input('数量入力', min_value=0, max_value=10, key='cont3')

        if parts3 != '':
            #部品名/単価/数量をリストに追加
            df_p3 = df_selected2_rank[df_selected2_rank['部品']==parts3]
            price3 = df_p3.iat[0, 2]

            name_list.append(parts3)
            price_list.append(price3)
            num_list.append(cont3)


        #********************************修理内容***************************************

        #*************品番リストの準備************************
        df = pd.read_excel('穂高修理価格表.xlsx')
        df_base = df.copy()

        naiyou_list = df_base['修理内容']
        #seriesのlist化
        naiyou_list = naiyou_list.values.tolist()
        naiyou_list.insert(0, '')

        #*****フォーム入力開始**********
        #*********************修理１********************************
        st.markdown('#### 修理内容入力フォーム')
        # *** selectbox 項目1***
        naiyou1 = st.selectbox(
            '■ 修理内容 1',
            naiyou_list,   
        )
        
        # selectbox 項目1
        cont_s1 = st.number_input('数量入力', min_value=0, max_value=10, key='cont_s1')

        if naiyou1 != '':
            #値をリストに追加
            df_n1 = df_base[df_base['修理内容']==naiyou1]
            price_n1 = df_n1.iat[0, 1]

            name_list.append(naiyou1)
            price_list.append(price_n1)
            num_list.append(cont_s1)

         #*********************修理2********************************
        naiyou2 = st.selectbox(
            '■ 修理内容 2',
            naiyou_list,   
        )
        
        # *** selectbox 項目2***
        cont_s2 = st.number_input('数量入力', min_value=0, max_value=10, key='cont_s2')

        if naiyou2 != '':
            #値をリストに追加
            df_n2 = df_base[df_base['修理内容']==naiyou2]
            price_n2 = df_n2.iat[0, 1]

            name_list.append(naiyou2)
            price_list.append(price_n2)
            num_list.append(cont_s2)

        #*********************修理3********************************
        naiyou3 = st.selectbox(
            '■ 修理内容 3',
            naiyou_list,   
        )
        
        cont_s3 = st.number_input('数量入力', min_value=0, max_value=10, key='cont_s3')

        if naiyou3 != '':
            #値をリストに追加
            df_n3 = df_base[df_base['修理内容']==naiyou3]
            price_n3 = df_n3.iat[0, 1]

            name_list.append(naiyou3)
            price_list.append(price_n3)
            num_list.append(cont_s3)

        #*********************修理4********************************
        naiyou4 = st.selectbox(
            '■ 修理内容 4',
            naiyou_list,   
        )
        
        # *** selectbox 項目4***
        cont_s4 = st.number_input('数量入力', min_value=0, max_value=10, key='cont_s4')

        if naiyou4 != '':
            #値をリストに追加
            df_n4 = df_base[df_base['修理内容']==naiyou4]
            price_n4 = df_n4.iat[0, 1]

            name_list.append(naiyou4)
            price_list.append(price_n4)
            num_list.append(cont_s4)

        #*********************修理5********************************
        naiyou5 = st.selectbox(
            '■ 修理内容 5',
            naiyou_list,   
        )
        
        # *** selectbox 項目5***
        cont_s5 = st.number_input('数量入力', min_value=0, max_value=10, key='cont_s5')

        if naiyou5 != '':
            #値をリストに追加
            df_n5 = df_base[df_base['修理内容']==naiyou5]
            price_n5 = df_n5.iat[0, 1]

            name_list.append(naiyou5)
            price_list.append(price_n5)
            num_list.append(cont_s5)

    #*****************************submitted**************************************************
    if submitted0:
        df_results = pd.DataFrame(list(zip(price_list, num_list)), columns=['単価', '数量'], index=name_list)
        df_results2 = df_results[df_results['数量'] >= 1]

        df_results2['小計'] = df_results2['単価'] * df_results2['数量']
        df_results2.loc['合計'] = df_results2['小計'].sum()
        
        df_results2.at['合計', '単価'] = 0
        df_results2.at['合計', '数量'] = 0
        df_results2.at['合計', '数量'] = df_results2['数量'].sum()

        df_results2['単価'] = df_results2['単価'].astype(int)
        df_results2['数量'] = df_results2['数量'].astype(int)
        df_results2['小計'] = df_results2['小計'].astype(int)
        df_results2['単価'] = df_results2['単価'].map(lambda x: '{:,}'.format(x))
        df_results2['小計'] = df_results2['小計'].map(lambda x: '{:,}'.format(x))
        st.table(df_results2)

        #***********備考表示***************
        df_comment = pd.read_excel('comment_hk.xlsx')

        if selected_item in list(df_comment['品番']):
            with st.expander('■ 備考'):
                df = df_comment[df_comment['品番']==selected_item]
                df_t = df.T
                df_t.dropna(how='any', inplace=True)
                st.table(df_t.iloc[1:])

        #****************修理注意点********************
        results_list = df_results2.index

        if '後脚欠け・脚折れ・背折れ(No.6各種/HK255各種)' in results_list:
            with st.expander('■ 修理注意点'):
                st.write('穂高リビングチェアの後脚接着ハガレの修理は、1969年~1984年までに製造したものは無償修理')
                st.write('往復送料は別途実費')

        if '回転軸交換(HK255AP・MM101AP)' in results_list:
            with st.expander('■ 回転盤交換修理注意点'):
                st.write('当時の回転盤が無いことがあるので要工場確認。（代替品対応）')
                st.write('注）回転盤の仕様が異なる場合、木部部分の削り加工が必要な場合がございます。その際はお預かり修理となります。') 

        for name in results_list:
            head2 = name[:2]
            if head2 == '塗装':
                with st.expander('■ 塗装修理注意点'):
                    st.write('再塗装修理は現在の塗装膜を手作業で落とし、研磨後に新たな塗装をします。')
                    st.write('注）色や艶を今使用している物、直した物そろえるのは難しいと事前にお伝えください。')
                    st.write('注）19●●年以前のものは旧K色指定。今とは色が違います。')
                    st.write('注）表面の生活傷は落ちますが、深い傷は落ちません。')
                    st.write('注）研磨しますので木目が変わります。')
                    st.write('注）同色での再塗装のみお受けさせて頂きます。（別色への変更不可）')

