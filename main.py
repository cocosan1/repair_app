import pandas as pd
import streamlit as st
import webbrowser
import glob
from PIL import Image

#st
st.set_page_config(page_title='修理見積もり')
st.markdown('#### チェア修理見積もりアプリ')
st.markdown('##### メニュー')

df_chair_all = pd.read_excel('chair_all.xlsx')
df_base = df_chair_all.copy()

df_base['品番'] =df_base['品番'].astype(str)
df_base['タイプ'] =df_base['タイプ'].astype(str)

df_base['A-S・A・B'] = df_base['A-S・A・B'].astype(int)
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
st.sidebar.markdown('#### 張り込みチェア見積')
selected_item = st.sidebar.selectbox(
    '品番:',
    item_list2,   
)    


if selected_item == '--品番を選択--':

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('###### 張り込みチェア修理見積')
        img0 = Image.open('img/張り修理.jpg')
        st.image(img0, width=150)
        st.write('サイドバーで品番を選択')

        st.markdown('###### 廃番品画像一覧')
        img1 = Image.open('img/昔カタログ.png')
        st.image(img1, width=150)
        link = '[廃番品画像一覧](http://repair-app-magnific.s3-website-ap-northeast-1.amazonaws.com/)'
        st.markdown(link, unsafe_allow_html=True)
        st.write('ここをクリック')

    with col2:
        st.markdown('###### ウインザーチェア（板座）修理見積')
        img1 = Image.open('img/板座修理.jpg')
        st.image(img1, width=150)
        st.write('サイドバー【windsor】をクリック')


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
        files = glob.glob("img\*.jpg")
        jpg_name = f'img\{selected_item}.jpg'
        if jpg_name in files:
            st.image(f'img\{selected_item}.jpg', width=60) 

    #品番でdfの絞り込み
    df_selected = df_base[df_base['品番']==selected_item]

    #布ランクリストの作成
    df_selected2 = df_selected[['品番', '部品', 'A-S・A・B', 'C', 'E', '本革A', '本革B']]

    #クッション価格一覧表示
    st.markdown('###### 張替え料金一覧')
    st.table(df_selected2)

    #***********備考表示***************
    df_comment = pd.read_excel('comment.xlsx')

    if selected_item in list(df_comment['品番']):
        with st.expander('■ 備考'):
            df = df_comment[df_comment['品番']==selected_item]
            df_t = df.T
            df_t.dropna(how='any', inplace=True)
            st.table(df_t)

    #*************品番リストの準備************************
    df = pd.read_excel('修理価格一覧app用.xlsx')
    df_base = df.copy()

    naiyou_list = df_base['修理内容']
    #seriesのlist化
    naiyou_list = naiyou_list.values.tolist()
    naiyou_list.insert(0, '')

    #****************ランク　数量入力フォーム*******************
    with st.sidebar.form(key='form0'):

        st.markdown('#### 計算ボタン')
        submitted0 = st.form_submit_button('計算')

        st.markdown('#### 張地ランク入力フォーム')
        # *** selectbox fabrank***
        fabrank_list = df_selected2.columns[2:]
    
        fabrank = st.selectbox(
            '■ 張地ランク',
            fabrank_list,   
        ) 
        # *** selectbox 項目1***
        cont0 = st.number_input('数量入力', min_value=0, max_value=10, key='cont0')

        #********************************修理内容***************************************
        st.markdown('#### 修理内容入力フォーム')
        # *** selectbox 項目1***
        naiyou1 = st.selectbox(
            '■ 修理内容 1',
            naiyou_list,   
        )
        
        # *** selectbox 項目1***
        cont1 = st.number_input('数量入力', min_value=0, max_value=10, key='cont1')

        # *** selectbox 項目2***
        naiyou2 = st.selectbox(
            '■ 修理内容 2',
            naiyou_list,   
        )
        
        # *** selectbox 項目2***
        cont2 = st.number_input('数量入力', min_value=0, max_value=10, key='cont2')

        # *** selectbox 項目3***
        naiyou3 = st.selectbox(
            '■ 修理内容 3',
            naiyou_list,   
        )
        
        # *** selectbox 項目3***
        cont3 = st.number_input('数量入力', min_value=0, max_value=10, key='cont3')

        # *** selectbox 項目4***
        naiyou4 = st.selectbox(
            '■ 修理内容 4',
            naiyou_list,   
        )
        
        # *** selectbox 項目4***
        cont4 = st.number_input('数量入力', min_value=0, max_value=10, key='cont4')

        # *** selectbox 項目5***
        naiyou5 = st.selectbox(
            '■ 修理内容 5',
            naiyou_list,   
        )
        
        # *** selectbox 項目5***
        cont5 = st.number_input('数量入力', min_value=0, max_value=10, key='cont5')

    df_fabcont = pd.DataFrame(index=['クッション張替え料金'])
    #*****************************submitted**************************************************
    if submitted0:

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

        df_fabcont['単価'] = fab_price

        #***********修理***************************************
        input_dict = {}
        if naiyou1 != '':
            input_dict[naiyou1] = cont1
        if naiyou2 != '':
            input_dict[naiyou2] = cont2
        if naiyou3 != '':
            input_dict[naiyou3] = cont3
        if naiyou4 != '':
            input_dict[naiyou4] = cont4
        if naiyou5 != '':
            input_dict[naiyou5] = cont5

        df_selected = pd.DataFrame(input_dict, index=['数量']).T
        df_results = df_base.merge(df_selected, left_on='修理内容', right_index=True, how='right')
        df_results.set_index('修理内容', drop=True, inplace=True)

        #クッション価格と数量のdf 
        df_fabcont['数量'] = cont0  

        df_results2 = pd.concat([df_fabcont, df_results], join='inner')
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

        results_list = df_results2.index

        if '組み直し修理' in results_list:
            with st.expander('■ 組み直し修理注意点'):
                st.write('木部の接合部分の緩みによるグラツキ等は一度部材を分解、組み直し接着をします。')
                st.write('注）接着剤が古いものはアンモニア系。現在は酢酸ビニール系で以前より丈夫です。')
                st.write('部材に破損が見られる場合は部材の修繕や交換となります。（部材代は別途）')
                st.write('注）接着剤が古いものはアンモニア系。現在は酢酸ビニール系で以前より丈夫です。')

        if 'ウインザー座割れ接着' in results_list:
            with st.expander('■ ウインザー座割れ接着注意点'):
                st.write('注）座面の裏に桟を取り付ける為、事前にお伝えください。')

        if '籐張り替え修理' in results_list:
            with st.expander('■ 籐張替修理注意点'):
                st.write('現在の籐を全て剥がし、新たな籐へ張替えをさせて頂きます。')
                st.write('注）塗装は致しますが天然の籐となりますのでお持ちのものと色が変わります。')
                st.write('注）修理後は少し硬く感じますがお使い頂く中で体になじんでいきます。') 

        if 'Dチェア再塗装' in results_list:
            with st.expander('■ 塗装修理注意点'):
                st.write('再塗装修理は現在の塗装膜を手作業で落とし、研磨後に新たな塗装をします。')
                st.write('注）色や艶を今使用している物、直した物そろえるのは難しいと事前にお伝えください。')
                st.write('注）19●●年以前のものは旧K色指定。今とは色が違います。')
                st.write('注）表面の生活傷は落ちますが、深い傷は落ちません。')
                st.write('注）研磨しますので木目が変わります。')
                st.write('注）同色での再塗装のみお受けさせて頂きます。（別色への変更不可）')
                st.write('注）同色での再塗装のみお受けさせて頂きます。（別色への変更不可）') 

        if 'アームチェア再塗装' in results_list:
            with st.expander('■ 塗装修理注意点'):
                st.write('再塗装修理は現在の塗装膜を手作業で落とし、研磨後に新たな塗装をします。')
                st.write('注）色や艶を今使用している物、直した物そろえるのは難しいと事前にお伝えください。')
                st.write('注）19●●年以前のものは旧K色指定。今とは色が違います。')
                st.write('注）表面の生活傷は落ちますが、深い傷は落ちません。')
                st.write('注）研磨しますので木目が変わります。')
                st.write('注）同色での再塗装のみお受けさせて頂きます。（別色への変更不可）')
                st.write('注）同色での再塗装のみお受けさせて頂きます。（別色への変更不可）') 

        if 'ウインザー回転盤交換修理' in results_list:
            with st.expander('■ 回転盤交換修理注意点'):
                st.write('当時の回転盤が無いことがあるので要工場確認。（代替品対応）')
                st.write('注）回転盤の仕様が異なる場合、木部部分の削り加工が必要な場合がございます。その際はお預かり修理となります。')                              


    


       

        
        