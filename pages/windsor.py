import pandas as pd
import streamlit as st
import webbrowser
import glob
from PIL import Image

#st
st.set_page_config(page_title='修理見積もり')
st.markdown('#### チェア修理見積もりアプリ')
st.markdown('##### ウインザーチェア（板座）')

img = Image.open('旧カタログ.png')
st.image(img, width=500)


df = pd.read_excel('修理価格一覧app用.xlsx')
df_base = df.copy()

naiyou_list = df_base['修理内容']
#seriesのlist化
naiyou_list = naiyou_list.values.tolist()
naiyou_list.insert(0, '')

st.sidebar.markdown('#### 入力フォーム')
with st.sidebar.form('入力フォーム'):

    st.markdown('#### 計算ボタン')
    submitted = st.form_submit_button('計算')
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

    
if submitted:
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
    df_results['小計'] = df_results['単価'] * df_results['数量']
    df_results.set_index('修理内容', drop=True, inplace=True)
    df_results.loc['合計'] = df_results['小計'].sum()
    df_results['単価'] = df_results['単価'].map(lambda x: '{:,}'.format(x))
    df_results['小計'] = df_results['小計'].map(lambda x: '{:,}'.format(x))
    df_results.at['合計', '単価'] = 0
    df_results.at['合計', '数量'] = 0
    df_results.at['合計', '数量'] = df_results['数量'].sum()
    st.table(df_results)

    results_list = df_results.index

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



    

    

    

     

    
                      






    

